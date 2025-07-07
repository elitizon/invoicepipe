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
