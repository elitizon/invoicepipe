# Step-by-Step Assignment: Building a Simple Invoice Processing Command Line Tool

## Goal
Create a simple command line tool that takes an invoice file (PDF, PNG, JPG, JPEG) as input and returns a structured JSON file containing extracted invoice data.

## Learning Objectives
By completing this assignment, you will:
- Build a CLI application using Python Click
- Integrate QuantaLogic PyZerox for document processing
- Work with environment variables and configuration
- Handle file I/O operations
- Create structured JSON output
- Apply error handling and validation
- Follow modern Python development practices

## Prerequisites
- Python 3.11+ installed
- Basic understanding of Python programming
- Familiarity with command line interfaces
- An API key for OpenAI, Gemini, or Anthropic (for document processing)

## Assignment Overview

You will build a CLI tool called `invoice-extractor` that:
1. Accepts an invoice file path as input
2. Validates the file format and existence
3. Processes the invoice using AI to extract structured data
4. Outputs the results as a JSON file
5. Provides helpful error messages and progress feedback

## Step 1: Project Setup (20 minutes)

### 1.1 Create Project Structure
```bash
mkdir invoice-extractor
cd invoice-extractor

# Create directory structure
mkdir -p src/invoice_extractor
mkdir -p tests
mkdir -p examples/invoices
mkdir -p examples/outputs
```

### 1.2 Create Virtual Environment
```bash
# Using UV (recommended)
uv venv
source .venv/bin/activate  # macOS/Linux
# or
.venv\Scripts\activate     # Windows

# Using standard Python
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
# or
.venv\Scripts\activate     # Windows
```

### 1.3 Create pyproject.toml
```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "invoice-extractor"
dynamic = ["version"]
description = "Simple CLI tool for extracting data from invoice documents"
readme = "README.md"
license = {text = "MIT"}
authors = [
    {name = "Your Name", email = "your.email@example.com"},
]
requires-python = ">=3.11"
dependencies = [
    "click>=8.1.0",
    "python-dotenv>=1.0.0",
    "quantalogic-py-zerox>=0.1.0",
    "pydantic>=2.5.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.4.0",
    "ruff>=0.1.0",
]

[project.scripts]
invoice-extractor = "invoice_extractor.cli:main"

[tool.hatch.version]
path = "src/invoice_extractor/__init__.py"

[tool.ruff]
line-length = 88
target-version = "py311"
```

### 1.4 Install Dependencies
```bash
# Using UV
uv pip install -e ".[dev]"

# Using pip
pip install -e ".[dev]"
```

## Step 2: Create Basic Project Files (15 minutes)

### 2.1 Create Version File
Create `src/invoice_extractor/__init__.py`:
```python
"""Invoice Extractor - Simple CLI tool for processing invoices."""

__version__ = "0.1.0"
```

### 2.2 Create Configuration
Create `src/invoice_extractor/config.py`:
```python
"""Configuration management for invoice extractor."""

import os
from typing import Optional
from pydantic import BaseSettings, Field

class Settings(BaseSettings):
    """Application settings."""
    
    # AI Provider Configuration
    openai_api_key: Optional[str] = Field(default=None, env="OPENAI_API_KEY")
    openai_model: str = Field(default="gpt-4o", env="OPENAI_MODEL")
    
    gemini_api_key: Optional[str] = Field(default=None, env="GEMINI_API_KEY")
    gemini_model: str = Field(default="gemini-2.0-flash-exp", env="GEMINI_MODEL")
    
    anthropic_api_key: Optional[str] = Field(default=None, env="ANTHROPIC_API_KEY")
    anthropic_model: str = Field(default="claude-3-5-sonnet-20241022", env="ANTHROPIC_MODEL")
    
    # File Processing
    supported_formats: list[str] = ["pdf", "png", "jpg", "jpeg"]
    max_file_size_mb: int = Field(default=10, env="MAX_FILE_SIZE_MB")
    
    @property
    def has_ai_provider(self) -> bool:
        """Check if at least one AI provider is configured."""
        return bool(self.openai_api_key or self.gemini_api_key or self.anthropic_api_key)
    
    def get_preferred_model(self) -> tuple[str, str]:
        """Get the preferred AI model and API key."""
        if self.openai_api_key:
            return self.openai_model, self.openai_api_key
        elif self.gemini_api_key:
            return self.gemini_model, self.gemini_api_key
        elif self.anthropic_api_key:
            return self.anthropic_model, self.anthropic_api_key
        else:
            raise ValueError("No AI provider configured")
    
    class Config:
        env_file = ".env"
        case_sensitive = True

# Global settings instance
settings = Settings()
```

### 2.3 Create Environment File
Create `.env`:
```env
# AI Provider Configuration (add your API key)
OPENAI_API_KEY=your-openai-api-key-here
OPENAI_MODEL=gpt-4o

# Alternative providers (optional)
# GEMINI_API_KEY=your-gemini-api-key-here
# ANTHROPIC_API_KEY=your-anthropic-api-key-here

# File Processing Settings
MAX_FILE_SIZE_MB=10
```

### 2.4 Create Environment Template
Create `.env.example`:
```env
# Copy this file to .env and add your API keys

# AI Provider Configuration (choose one)
OPENAI_API_KEY=your-openai-api-key-here
OPENAI_MODEL=gpt-4o

# Alternative providers
GEMINI_API_KEY=your-gemini-api-key-here
GEMINI_MODEL=gemini-2.0-flash-exp

ANTHROPIC_API_KEY=your-anthropic-api-key-here
ANTHROPIC_MODEL=claude-3-5-sonnet-20241022

# File Processing Settings
MAX_FILE_SIZE_MB=10
```

## Step 3: Create Data Models (15 minutes)

### 3.1 Create Invoice Data Models
Create `src/invoice_extractor/models.py`:
```python
"""Data models for invoice processing."""

from datetime import date
from decimal import Decimal
from typing import List, Optional
from pydantic import BaseModel, Field


class Address(BaseModel):
    """Address information."""
    street: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip_code: Optional[str] = None
    country: Optional[str] = None


class Entity(BaseModel):
    """Business entity (vendor or customer)."""
    name: Optional[str] = None
    address: Optional[Address] = None
    tax_id: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None


class LineItem(BaseModel):
    """Invoice line item."""
    description: Optional[str] = None
    quantity: Optional[Decimal] = None
    unit_price: Optional[Decimal] = None
    total: Optional[Decimal] = None
    tax_rate: Optional[Decimal] = None


class Totals(BaseModel):
    """Invoice totals."""
    subtotal: Optional[Decimal] = None
    tax: Optional[Decimal] = None
    total: Optional[Decimal] = None
    currency: str = "USD"


class InvoiceData(BaseModel):
    """Complete invoice data structure."""
    invoice_number: Optional[str] = None
    date: Optional[date] = None
    due_date: Optional[date] = None
    vendor: Optional[Entity] = None
    customer: Optional[Entity] = None
    totals: Optional[Totals] = None
    line_items: List[LineItem] = []
    notes: Optional[str] = None
    payment_terms: Optional[str] = None


class ProcessingResult(BaseModel):
    """Result of invoice processing."""
    success: bool
    invoice_data: Optional[InvoiceData] = None
    error_message: Optional[str] = None
    processing_time: Optional[float] = None
    confidence_score: Optional[float] = None
```

## Step 4: Create File Validation Utilities (20 minutes)

### 4.1 Create Validation Module
Create `src/invoice_extractor/validators.py`:
```python
"""File validation utilities."""

import os
import magic
from pathlib import Path
from typing import Tuple

from .config import settings


def validate_file_exists(file_path: str) -> bool:
    """Check if file exists."""
    return Path(file_path).exists()


def validate_file_size(file_path: str) -> Tuple[bool, str]:
    """Validate file size."""
    file_size = os.path.getsize(file_path)
    max_size = settings.max_file_size_mb * 1024 * 1024  # Convert to bytes
    
    if file_size > max_size:
        return False, f"File size ({file_size / 1024 / 1024:.1f}MB) exceeds limit ({settings.max_file_size_mb}MB)"
    
    return True, ""


def validate_file_format(file_path: str) -> Tuple[bool, str]:
    """Validate file format using magic numbers."""
    try:
        mime_type = magic.from_file(file_path, mime=True)
        
        # Map MIME types to our supported formats
        supported_mime_types = {
            "application/pdf": "pdf",
            "image/png": "png",
            "image/jpeg": "jpg",
            "image/jpg": "jpg",
        }
        
        if mime_type not in supported_mime_types:
            return False, f"Unsupported file type: {mime_type}"
        
        detected_format = supported_mime_types[mime_type]
        if detected_format not in settings.supported_formats:
            return False, f"Format {detected_format} not supported"
        
        return True, detected_format
    
    except Exception as e:
        return False, f"Error detecting file type: {str(e)}"


def validate_invoice_file(file_path: str) -> Tuple[bool, str]:
    """Comprehensive file validation."""
    # Check if file exists
    if not validate_file_exists(file_path):
        return False, f"File not found: {file_path}"
    
    # Validate file size
    size_valid, size_error = validate_file_size(file_path)
    if not size_valid:
        return False, size_error
    
    # Validate file format
    format_valid, format_result = validate_file_format(file_path)
    if not format_valid:
        return False, format_result
    
    return True, f"Valid {format_result} file"
```

**Note**: You'll need to install `python-magic` for file type detection:
```bash
# Add to pyproject.toml dependencies
python-magic>=0.4.27

# Install system dependencies
# macOS:
brew install libmagic
# Ubuntu:
sudo apt-get install libmagic1
```

## Step 5: Create Document Processor (30 minutes)

### 5.1 Create Processor Module
Create `src/invoice_extractor/processor.py`:
```python
"""Document processing using QuantaLogic PyZerox."""

import asyncio
import os
import time
from typing import Optional

from pyzerox import zerox
from .config import settings
from .models import InvoiceData, ProcessingResult


class InvoiceProcessor:
    """Invoice document processor."""
    
    def __init__(self):
        """Initialize processor with AI configuration."""
        if not settings.has_ai_provider:
            raise ValueError("No AI provider configured. Please set API keys in .env file.")
        
        self.model, self.api_key = settings.get_preferred_model()
        self._setup_environment()
    
    def _setup_environment(self):
        """Set up environment variables for the AI provider."""
        if "gpt" in self.model.lower():
            os.environ["OPENAI_API_KEY"] = self.api_key
        elif "gemini" in self.model.lower():
            os.environ["GEMINI_API_KEY"] = self.api_key
        elif "claude" in self.model.lower():
            os.environ["ANTHROPIC_API_KEY"] = self.api_key
    
    async def process_invoice(self, file_path: str) -> ProcessingResult:
        """Process invoice file and extract structured data."""
        start_time = time.time()
        
        try:
            # Custom system prompt for invoice extraction
            system_prompt = """
            You are an expert invoice data extraction system. 
            Extract structured data from the provided invoice document.
            
            Please extract the following information:
            - Invoice number
            - Date and due date
            - Vendor/supplier information (name, address, tax ID, contact info)
            - Customer/bill-to information (name, address)
            - Line items with descriptions, quantities, unit prices, and totals
            - Subtotal, tax amounts, and total
            - Payment terms and notes
            
            Return the data in a structured JSON format that matches the expected schema.
            Be precise with numbers and dates. If information is not available, use null.
            """
            
            # Process with PyZerox
            result = await zerox(
                file_path=file_path,
                model=self.model,
                cleanup=True,
                custom_system_prompt=system_prompt,
                maintain_format=False,
                **{"temperature": 0.1}  # Lower temperature for more consistent output
            )
            
            # Extract the content
            if result and hasattr(result, 'content'):
                content = result.content
            else:
                content = str(result)
            
            # Parse the result into our data model
            invoice_data = self._parse_extracted_data(content)
            
            processing_time = time.time() - start_time
            
            return ProcessingResult(
                success=True,
                invoice_data=invoice_data,
                processing_time=processing_time,
                confidence_score=0.9  # PyZerox doesn't provide confidence scores
            )
        
        except Exception as e:
            processing_time = time.time() - start_time
            return ProcessingResult(
                success=False,
                error_message=f"Processing failed: {str(e)}",
                processing_time=processing_time
            )
    
    def _parse_extracted_data(self, content: str) -> InvoiceData:
        """Parse extracted content into structured invoice data."""
        try:
            # This is a simplified parser - in a real application,
            # you'd want more sophisticated parsing logic
            
            # For now, create a basic invoice data structure
            # In practice, you'd parse the AI response more carefully
            
            return InvoiceData(
                invoice_number="Extracted from AI response",
                notes=f"Raw extracted content: {content[:500]}..."  # Truncate for example
            )
        
        except Exception as e:
            # Return minimal data if parsing fails
            return InvoiceData(
                notes=f"Parsing error: {str(e)}. Raw content: {content[:200]}..."
            )
    
    def process_invoice_sync(self, file_path: str) -> ProcessingResult:
        """Synchronous wrapper for processing."""
        return asyncio.run(self.process_invoice(file_path))
```

## Step 6: Create CLI Interface (25 minutes)

### 6.1 Create CLI Module
Create `src/invoice_extractor/cli.py`:
```python
"""Command line interface for invoice extractor."""

import json
import sys
from pathlib import Path
from typing import Optional

import click
from dotenv import load_dotenv

from .config import settings
from .processor import InvoiceProcessor
from .validators import validate_invoice_file

# Load environment variables
load_dotenv()


@click.command()
@click.argument("input_file", type=click.Path(exists=True))
@click.option(
    "--output", "-o",
    type=click.Path(),
    help="Output JSON file path (default: input_file.json)"
)
@click.option(
    "--pretty", "-p",
    is_flag=True,
    help="Pretty-print JSON output"
)
@click.option(
    "--verbose", "-v",
    is_flag=True,
    help="Enable verbose output"
)
@click.version_option()
def main(input_file: str, output: Optional[str], pretty: bool, verbose: bool):
    """
    Extract structured data from invoice documents.
    
    Takes an invoice file (PDF, PNG, JPG, JPEG) as input and outputs JSON.
    
    Example:
    
        invoice-extractor invoice.pdf
        
        invoice-extractor invoice.pdf --output result.json --pretty
    """
    # Print banner
    if verbose:
        click.echo("🧾 Invoice Extractor CLI")
        click.echo("=" * 50)
    
    # Validate configuration
    if not settings.has_ai_provider:
        click.echo("❌ Error: No AI provider configured.", err=True)
        click.echo("Please set API keys in .env file:", err=True)
        click.echo("  - OPENAI_API_KEY for OpenAI GPT models", err=True)
        click.echo("  - GEMINI_API_KEY for Google Gemini models", err=True)
        click.echo("  - ANTHROPIC_API_KEY for Anthropic Claude models", err=True)
        sys.exit(1)
    
    # Validate input file
    if verbose:
        click.echo(f"📄 Validating file: {input_file}")
    
    is_valid, validation_message = validate_invoice_file(input_file)
    if not is_valid:
        click.echo(f"❌ File validation failed: {validation_message}", err=True)
        sys.exit(1)
    
    if verbose:
        click.echo(f"✅ {validation_message}")
    
    # Determine output file
    if output is None:
        input_path = Path(input_file)
        output = input_path.with_suffix('.json')
    
    if verbose:
        click.echo(f"📤 Output file: {output}")
        click.echo(f"🤖 Using AI model: {settings.get_preferred_model()[0]}")
    
    # Process the invoice
    try:
        if verbose:
            click.echo("🔄 Processing invoice...")
        
        processor = InvoiceProcessor()
        result = processor.process_invoice_sync(input_file)
        
        if not result.success:
            click.echo(f"❌ Processing failed: {result.error_message}", err=True)
            sys.exit(1)
        
        # Prepare output data
        output_data = {
            "success": result.success,
            "processing_time": result.processing_time,
            "confidence_score": result.confidence_score,
            "invoice_data": result.invoice_data.model_dump() if result.invoice_data else None,
            "metadata": {
                "input_file": str(input_file),
                "output_file": str(output),
                "model_used": settings.get_preferred_model()[0]
            }
        }
        
        # Write output file
        with open(output, 'w', encoding='utf-8') as f:
            if pretty:
                json.dump(output_data, f, indent=2, ensure_ascii=False, default=str)
            else:
                json.dump(output_data, f, ensure_ascii=False, default=str)
        
        # Success message
        click.echo(f"✅ Processing completed successfully!")
        if verbose:
            click.echo(f"⏱️  Processing time: {result.processing_time:.2f} seconds")
            click.echo(f"📊 Confidence score: {result.confidence_score:.2f}")
        click.echo(f"💾 Output saved to: {output}")
        
    except Exception as e:
        click.echo(f"❌ Unexpected error: {str(e)}", err=True)
        if verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
```

## Step 7: Create Tests (20 minutes)

### 7.1 Create Test Configuration
Create `tests/conftest.py`:
```python
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
```

### 7.2 Create Validation Tests
Create `tests/test_validators.py`:
```python
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
```

### 7.3 Create CLI Tests
Create `tests/test_cli.py`:
```python
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
```

## Step 8: Create Documentation and Examples (15 minutes)

### 8.1 Create README
Create `README.md`:
```markdown
# Invoice Extractor CLI

A simple command-line tool for extracting structured data from invoice documents using AI.

## Features

- Extract data from PDF, PNG, JPG, and JPEG invoice files
- Support for multiple AI providers (OpenAI, Gemini, Anthropic)
- Structured JSON output
- File validation and error handling
- Configurable via environment variables

## Installation

1. Clone the repository
2. Create a virtual environment and activate it
3. Install dependencies:
   ```bash
   pip install -e .
   ```

## Configuration

1. Copy `.env.example` to `.env`
2. Add your AI provider API key:
   ```env
   OPENAI_API_KEY=your-api-key-here
   ```

## Usage

Basic usage:
```bash
invoice-extractor invoice.pdf
```

With options:
```bash
invoice-extractor invoice.pdf --output result.json --pretty --verbose
```

## Options

- `--output, -o`: Specify output file (default: input_file.json)
- `--pretty, -p`: Pretty-print JSON output
- `--verbose, -v`: Enable verbose output
- `--help`: Show help message

## Examples

Process a PDF invoice:
```bash
invoice-extractor examples/invoices/sample.pdf
```

Process with custom output:
```bash
invoice-extractor invoice.pdf -o extracted_data.json --pretty
```

## Testing

Run tests:
```bash
pytest
```

Run tests with coverage:
```bash
pytest --cov=invoice_extractor
```
```

### 8.2 Create Example Invoice
Create `examples/invoices/README.md`:
```markdown
# Example Invoices

This directory contains sample invoice files for testing the invoice extractor.

## Files

- `sample.pdf` - Sample PDF invoice
- `sample.png` - Sample PNG invoice image

## Usage

Process the sample invoice:
```bash
invoice-extractor examples/invoices/sample.pdf --verbose --pretty
```

The output will be saved as `examples/invoices/sample.json`.
```

## Step 9: Testing Your Implementation (15 minutes)

### 9.1 Manual Testing Checklist

1. **Environment Setup**
   - [ ] Virtual environment activated
   - [ ] Dependencies installed
   - [ ] `.env` file created with API key
   - [ ] CLI command accessible

2. **Basic Functionality**
   - [ ] Run `invoice-extractor --help`
   - [ ] Test with non-existent file (should show error)
   - [ ] Test with unsupported file format (should show error)
   - [ ] Test with valid invoice file (should create JSON output)

3. **CLI Options**
   - [ ] Test `--verbose` flag
   - [ ] Test `--pretty` flag
   - [ ] Test `--output` custom path
   - [ ] Test with various file formats (PDF, PNG, JPG)

4. **Output Validation**
   - [ ] Check JSON file is created
   - [ ] Verify JSON structure matches expected format
   - [ ] Check metadata is included
   - [ ] Verify processing time is recorded

### 9.2 Test Commands

```bash
# Test help
invoice-extractor --help

# Test with verbose output
invoice-extractor examples/invoices/sample.pdf --verbose --pretty

# Test with custom output
invoice-extractor examples/invoices/sample.pdf -o custom_output.json

# Run automated tests
pytest tests/ -v
```

## Step 10: Enhancement Ideas (Optional)

Once you have the basic tool working, consider these enhancements:

1. **Add more AI providers support**
2. **Implement batch processing for multiple files**
3. **Add configuration validation**
4. **Create a web interface**
5. **Add result confidence scoring**
6. **Support for different output formats (CSV, YAML)**
7. **Add invoice template recognition**
8. **Implement caching for processed files**

## Advanced Enhancement: Instructor Library Integration

### Overview
For students who want to explore advanced AI development patterns, we recommend integrating the [Instructor library](https://python.useinstructor.com/) to enhance the invoice processing pipeline. This optional enhancement teaches industry-standard structured data extraction patterns.

### Why Use Instructor?
- **Structured Data Extraction**: Define precise Pydantic models for invoice data
- **Automatic Validation**: Built-in retry logic when validation fails
- **Multi-Provider Support**: Works with OpenAI, Anthropic, Google, and 15+ LLM providers
- **Production-Ready**: Streaming, caching, and comprehensive error handling

### Integration Steps

#### 1. Install Instructor
```bash
# Add to pyproject.toml dependencies
instructor>=1.0.0

# Or install directly
pip install instructor
```

#### 2. Enhanced Data Models
Replace basic data models with Instructor-optimized versions:

```python
# src/invoice_extractor/models.py
import instructor
from pydantic import BaseModel, Field, validator
from typing import List, Optional
from datetime import date
from decimal import Decimal

class InvoiceItem(BaseModel):
    """Enhanced invoice item with validation."""
    description: str = Field(..., description="Item description")
    quantity: Decimal = Field(..., gt=0, description="Quantity (must be positive)")
    unit_price: Decimal = Field(..., ge=0, description="Unit price")
    total: Decimal = Field(..., ge=0, description="Line total")
    
    @validator('total')
    def validate_total(cls, v, values):
        """Validate that total = quantity * unit_price."""
        if 'quantity' in values and 'unit_price' in values:
            expected_total = values['quantity'] * values['unit_price']
            if abs(v - expected_total) > 0.01:
                raise ValueError(f"Total {v} doesn't match quantity × unit_price ({expected_total})")
        return v

class EnhancedInvoiceData(BaseModel):
    """Enhanced invoice data with automatic validation."""
    invoice_number: str = Field(..., description="Invoice number")
    date: date = Field(..., description="Invoice date")
    vendor_name: str = Field(..., description="Vendor/supplier name")
    customer_name: str = Field(..., description="Customer name")
    items: List[InvoiceItem] = Field(..., min_items=1, description="Invoice line items")
    subtotal: Decimal = Field(..., ge=0, description="Subtotal amount")
    tax: Decimal = Field(..., ge=0, description="Tax amount")
    total: Decimal = Field(..., ge=0, description="Total amount")
    currency: str = Field(default="USD", description="Currency code")
    
    @validator('total')
    def validate_total_amount(cls, v, values):
        """Validate that total = subtotal + tax."""
        if 'subtotal' in values and 'tax' in values:
            expected_total = values['subtotal'] + values['tax']
            if abs(v - expected_total) > 0.01:
                raise ValueError(f"Total {v} doesn't match subtotal + tax ({expected_total})")
        return v
```

#### 3. Enhanced Processor
Create an Instructor-powered processor:

```python
# src/invoice_extractor/instructor_processor.py
import instructor
from openai import OpenAI
from .models import EnhancedInvoiceData

class InstructorInvoiceProcessor:
    """Invoice processor using Instructor library."""
    
    def __init__(self, api_key: str, model: str = "gpt-4o"):
        self.client = instructor.from_openai(OpenAI(api_key=api_key))
        self.model = model
    
    def extract_invoice_data(self, text_content: str) -> EnhancedInvoiceData:
        """Extract structured invoice data with automatic validation."""
        try:
            return self.client.chat.completions.create(
                model=self.model,
                response_model=EnhancedInvoiceData,
                messages=[
                    {
                        "role": "system",
                        "content": """You are an expert invoice data extractor. 
                        Extract all relevant information from the provided invoice text.
                        Be precise with numbers and dates."""
                    },
                    {
                        "role": "user",
                        "content": f"Extract structured data from this invoice:\n\n{text_content}"
                    }
                ],
                max_retries=3,  # Automatic retry on validation failure
            )
        except Exception as e:
            raise ValueError(f"Failed to extract invoice data: {str(e)}")
    
    def extract_with_streaming(self, text_content: str):
        """Extract with streaming for real-time updates."""
        for partial_invoice in self.client.chat.completions.create_partial(
            model=self.model,
            response_model=EnhancedInvoiceData,
            messages=[
                {"role": "user", "content": f"Extract invoice data: {text_content}"}
            ]
        ):
            yield partial_invoice
```

#### 4. Enhanced CLI Options
Add advanced CLI options:

```python
@click.option('--use-instructor', is_flag=True, help='Use Instructor library for enhanced extraction')
@click.option('--stream', is_flag=True, help='Enable streaming output')
@click.option('--provider', default='openai', help='LLM provider (openai, anthropic, google)')
def extract_invoice(invoice_file, output, use_instructor, stream, provider):
    """Enhanced CLI with Instructor support."""
    if use_instructor:
        processor = InstructorInvoiceProcessor()
        if stream:
            click.echo("Processing with streaming...")
            for partial_data in processor.extract_with_streaming(text_content):
                click.echo(f"Processing: {partial_data.invoice_number or 'Working...'}")
        else:
            result = processor.extract_invoice_data(text_content)
    else:
        # Use original processor
        processor = InvoiceProcessor()
        result = processor.process_invoice(invoice_file)
```

### Benefits of Using Instructor

1. **Automatic Validation**: Ensures data quality without manual validation code
2. **Retry Logic**: Automatically retries failed extractions with improved prompts
3. **Type Safety**: Full IDE support with autocomplete and type checking
4. **Multi-Provider**: Easy to switch between OpenAI, Anthropic, Google, etc.
5. **Streaming Support**: Real-time processing for better user experience
6. **Production Patterns**: Learn industry-standard AI development practices

### Advanced Challenges

For students using Instructor, try these additional challenges:

1. **Custom Validators**: Add business logic validation using Pydantic validators
2. **Multi-Provider Support**: Implement support for different LLM providers
3. **Batch Processing**: Process multiple invoices efficiently
4. **Error Recovery**: Implement fallback strategies for failed extractions
5. **Performance Optimization**: Add caching and response optimization

### Learning Resources

- [Instructor Documentation](https://python.useinstructor.com/) - Complete guide and examples
- [Instructor Integration Guide](../instructor-integration-guide.md) - Detailed implementation guide
- [Receipt Processing Example](https://python.useinstructor.com/examples/extracting_receipts/) - Similar use case
- [Pydantic Validation](https://docs.pydantic.dev/latest/concepts/validators/) - Advanced validation patterns

### When to Use Instructor

Consider using Instructor when:
- Building production-ready AI applications
- Need reliable structured data extraction
- Want automatic validation and retry logic
- Working with multiple LLM providers
- Require real-time streaming capabilities

This enhancement transforms the assignment from a basic text processing exercise into a comprehensive, production-ready AI application that teaches modern development patterns.

---
