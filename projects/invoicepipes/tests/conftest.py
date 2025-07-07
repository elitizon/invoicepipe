"""Test configuration and fixtures."""

import pytest
import tempfile
from pathlib import Path
from unittest.mock import patch

from invoice_extractor.config import Settings
from invoice_extractor.models import InvoiceData, ProcessingResult


@pytest.fixture
def test_settings():
    """Test settings with mock configuration."""
    return Settings(
        openai_api_key="test-key",
        openai_model="gpt-4o",
        max_file_size_mb=5
    )


@pytest.fixture
def sample_invoice_data():
    """Sample invoice data for testing."""
    return InvoiceData(
        invoice_number="INV-2024-001",
        notes="Test invoice data"
    )


@pytest.fixture
def temp_pdf_file():
    """Create a temporary PDF file for testing."""
    with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as f:
        # Write minimal PDF content
        f.write(b"%PDF-1.4\n1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n")
        temp_path = f.name
    
    yield temp_path
    
    # Cleanup
    Path(temp_path).unlink(missing_ok=True)


@pytest.fixture
def temp_json_file():
    """Create a temporary JSON file for testing."""
    with tempfile.NamedTemporaryFile(suffix='.json', delete=False) as f:
        temp_path = f.name
    
    yield temp_path
    
    # Cleanup
    Path(temp_path).unlink(missing_ok=True)
