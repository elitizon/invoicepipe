# InvoicePipe

## WHY

Manual invoice processing is time-consuming, error-prone, and costly. InvoicePipe aims to automate the extraction and structuring of data from invoices and similar documents, enabling businesses to streamline their accounting workflows, reduce human error, and accelerate financial operations.

## WHAT

InvoicePipe is a Python-based project designed to analyze and extract structured data from PDF and image invoices using state-of-the-art AI models. It leverages the [QuantaLogic PyZerox](https://github.com/quantalogic/quantalogic-pyzerox) toolkit for document analysis, supporting a wide range of file types and vision-capable LLMs (OpenAI GPT-4o, Gemini, Claude, etc.).

Key features:
- Automated extraction of invoice data from PDFs and images
- Support for multiple AI vision models
- Batch processing of documents
- Customizable extraction prompts and options

## HOW

1. **Install dependencies**
   - Python 3.8+
   - System tools for PDF/image processing (see documentation)
   - Install Python requirements: `pip install py-zerox`
2. **Configure your API key** for a supported vision model (e.g., OpenAI, Gemini, Claude)
3. **Run the extraction script** on your invoice files (see usage examples in the documentation)

For detailed setup and usage instructions, see:
- [Using QuantaLogic PyZerox to Analyze PDFs and Images](docs/using-quantalogic-pyzerox.md)
- [InvoicePipe Specification](docs/spec-invoice.md)
- [Setting Up a FastAPI Project with Modern Python Tooling](docs/setup-fastapi-project.md)
- [Managing Environment Variables and Configuration](docs/managing-env-files.md)

---

For more information on supported models, file types, and advanced options, refer to the [QuantaLogic PyZerox documentation](https://github.com/quantalogic/quantalogic-pyzerox).
