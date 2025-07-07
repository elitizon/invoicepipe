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

## Usage

```bash
invoice-extractor invoice.pdf --output result.json --pretty --verbose
```

## Configuration

Copy `.env.example` to `.env` and add your API keys:

```env
OPENAI_API_KEY=your-openai-api-key-here
OPENAI_MODEL=gpt-4o
# GEMINI_API_KEY=your-gemini-api-key-here
# ANTHROPIC_API_KEY=your-anthropic-api-key-here
MAX_FILE_SIZE_MB=10
```

## Example

```bash
invoice-extractor invoice.pdf --output invoice.json --pretty --verbose
```

## Testing

```bash
pytest
```

## License

MIT
