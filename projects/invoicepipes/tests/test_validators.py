"""Test file validation functions."""

import pytest
from unittest.mock import patch, mock_open
from pathlib import Path

from invoice_extractor.validators import (
    validate_file_exists,
    validate_file_size,
    validate_file_format,
    validate_invoice_file
)


def test_validate_file_exists(tmp_path):
    """Test file existence validation."""
    # Create a temporary file
    test_file = tmp_path / "test.pdf"
    test_file.write_text("test content")
    
    # Test existing file
    assert validate_file_exists(str(test_file)) is True
    
    # Test non-existing file
    assert validate_file_exists(str(tmp_path / "nonexistent.pdf")) is False


def test_validate_file_size(tmp_path):
    """Test file size validation."""
    # Create a small file
    small_file = tmp_path / "small.pdf"
    small_file.write_text("small content")
    
    # Test small file (should pass)
    is_valid, message = validate_file_size(str(small_file))
    assert is_valid is True
    assert message == ""


@patch('invoice_extractor.validators.magic.from_file')
def test_validate_file_format(mock_magic):
    """Test file format validation."""
    # Test PDF file
    mock_magic.return_value = "application/pdf"
    is_valid, format_type = validate_file_format("test.pdf")
    assert is_valid is True
    assert format_type == "pdf"
    
    # Test unsupported format
    mock_magic.return_value = "application/msword"
    is_valid, error = validate_file_format("test.doc")
    assert is_valid is False
    assert "Unsupported file type" in error


def test_validate_invoice_file_success(tmp_path):
    """Test successful invoice file validation."""
    # Create test file
    test_file = tmp_path / "test.pdf"
    test_file.write_text("test content")
    
    with patch('invoice_extractor.validators.magic.from_file', return_value="application/pdf"):
        is_valid, message = validate_invoice_file(str(test_file))
        assert is_valid is True
        assert "Valid pdf file" in message


def test_validate_invoice_file_not_found():
    """Test validation with non-existent file."""
    is_valid, message = validate_invoice_file("nonexistent.pdf")
    assert is_valid is False
    assert "File not found" in message
