# Using QuantaLogic PyZerox to Analyze PDFs and Images

[QuantaLogic PyZerox](https://github.com/quantalogic/quantalogic-pyzerox) is a cross-platform toolkit for AI-powered document analysis, supporting PDF, images, and many other formats. It leverages vision-capable LLMs (like OpenAI GPT-4o, Gemini, Claude, etc.) to extract structured data from documents.

## Prerequisites

- Python 3.8+
- Install system dependencies (for PDF/image processing):
  - macOS: `brew install poppler graphicsmagick ghostscript`
  - Ubuntu: `sudo apt-get install -y poppler-utils graphicsmagick ghostscript`
- Obtain an API key for a supported vision model (e.g., OpenAI, Gemini, Claude, Azure, Bedrock)

## Installation

```bash
pip install py-zerox
```

## Basic Usage Example (Python)

This example shows how to analyze a PDF or image file and print the extracted result as JSON.

```python
import asyncio
from pyzerox import zerox
import os

# Set your API key (example for OpenAI)
os.environ["OPENAI_API_KEY"] = "your-api-key-here"

async def main():
    result = await zerox(
        file_path="path/to/your/document.pdf",  # or .png, .jpg, etc.
        model="gpt-4o"  # Use a vision-capable model
    )
    print(result)

asyncio.run(main())
```

## Advanced Usage Example

You can customize processing with additional options:

```python
import asyncio
from pyzerox import zerox
import os

os.environ["OPENAI_API_KEY"] = "your-api-key-here"

async def main():
    result = await zerox(
        file_path="path/to/your/invoice.png",
        model="gpt-4o-mini",
        cleanup=True,           # Clean up temp files after processing
        concurrency=5,          # Number of pages to process in parallel
        maintain_format=False,  # Set True to preserve layout (slower)
        select_pages=None,      # Process all pages, or specify [1,2,3]
        output_dir=None,        # Save output files if needed
        custom_system_prompt=None,  # Custom prompt for extraction
        **{"temperature": 0.1}    # Model-specific parameters
    )
    print(result)

asyncio.run(main())
```

## Batch Processing Example

Process multiple documents in a directory:

```python
import asyncio
from pyzerox import zerox
import os
import glob

os.environ["OPENAI_API_KEY"] = "your-api-key-here"

async def process_documents(file_paths):
    results = []
    for file_path in file_paths:
        result = await zerox(
            file_path=file_path,
            model="gpt-4o-mini",
            output_dir="./processed"
        )
        results.append(result)
    return results

files = glob.glob("./invoices/*.[pj][pn]g") + glob.glob("./invoices/*.pdf")
results = asyncio.run(process_documents(files))
```

## Supported Models and Providers

- OpenAI: `gpt-4o`, `gpt-4o-mini`, `gpt-4-turbo`, etc.
- Google Gemini: `gemini/gemini-2.5-flash`, etc.
- Anthropic Claude: `claude-sonnet-4-20250514`, etc.
- Azure OpenAI, AWS Bedrock, and more

See the [official documentation](https://github.com/quantalogic/quantalogic-pyzerox#-supported-vision-models) for the latest supported models and configuration details.

## Supported File Types

- PDF, PNG, JPG, JPEG, TIFF, BMP, SVG, WEBP, and more

## Tips

- Always use a vision-capable model for document/image analysis.
- For best results, use high-quality scans or images.
- You can provide a custom prompt to guide extraction for specific layouts.

---

## Related Documentation

- [InvoicePipe Project Overview](../README.md)
- [InvoicePipe Specification](spec-invoice.md)
- [Setting Up a FastAPI Project with Modern Python Tooling](setup-fastapi-project.md)

For more details, see the [QuantaLogic PyZerox documentation](https://github.com/quantalogic/quantalogic-pyzerox).
