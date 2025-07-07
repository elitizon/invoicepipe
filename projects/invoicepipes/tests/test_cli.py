"""Test CLI interface."""

import json
import pytest
from click.testing import CliRunner
from unittest.mock import patch, MagicMock

from invoice_extractor.cli import main
from invoice_extractor.models import ProcessingResult, InvoiceData


@pytest.fixture
def cli_runner():
    """CLI test runner."""
    return CliRunner()


def test_cli_no_api_key(cli_runner, tmp_path):
    """Test CLI behavior without API key."""
    test_file = tmp_path / "test.pdf"
    test_file.write_text("test")
    
    with patch('invoice_extractor.config.settings.has_ai_provider', False):
        result = cli_runner.invoke(main, [str(test_file)])
        assert result.exit_code == 1
        assert "No AI provider configured" in result.output


def test_cli_invalid_file(cli_runner):
    """Test CLI with invalid file."""
    result = cli_runner.invoke(main, ["nonexistent.pdf"])
    assert result.exit_code == 2  # Click's file not found error


@patch('invoice_extractor.cli.InvoiceProcessor')
@patch('invoice_extractor.cli.validate_invoice_file')
@patch('invoice_extractor.config.settings.has_ai_provider', True)
def test_cli_success(mock_validate, mock_processor, cli_runner, tmp_path):
    """Test successful CLI processing."""
    # Setup mocks
    mock_validate.return_value = (True, "Valid pdf file")
    
    mock_processor_instance = MagicMock()
    mock_processor.return_value = mock_processor_instance
    
    test_invoice = InvoiceData(invoice_number="TEST-001")
    mock_result = ProcessingResult(
        success=True,
        invoice_data=test_invoice,
        processing_time=1.5,
        confidence_score=0.9
    )
    mock_processor_instance.process_invoice_sync.return_value = mock_result
    
    # Create test file
    test_file = tmp_path / "test.pdf"
    test_file.write_text("test content")
    
    # Run CLI
    result = cli_runner.invoke(main, [str(test_file), "--verbose"])
    
    # Check results
    assert result.exit_code == 0
    assert "Processing completed successfully" in result.output
    
    # Check output file was created
    output_file = tmp_path / "test.json"
    assert output_file.exists()
    
    # Verify output content
    with open(output_file) as f:
        output_data = json.load(f)
    
    assert output_data["success"] is True
    assert output_data["processing_time"] == 1.5
    assert output_data["invoice_data"]["invoice_number"] == "TEST-001"
