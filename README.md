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

## 🗂️ Directory Structure

```
invoicepipe/
├── .git/                       # Git repository data
├── .gitignore                  # Git ignore rules
├── .venv/                      # Python virtual environment (optional)
├── .vscode/                    # VS Code settings
├── README.md                   # Project overview and instructions
├── docs/                       # Documentation, guides, cheat sheets
│   ├── git-github-cheat-sheet.md
│   ├── instructor-integration-guide.md
│   ├── litellm-integration-guide.md
│   ├── managing-env-files.md
│   ├── setup-fastapi-project.md
│   ├── spec-invoice.md
│   ├── using-quantalogic-pyzerox.md
│   └── preparation-work/
│       └── step-by-step-assignment.md
├── projects/                   # Project modules and experiments
│   └── invoicepipes/           # (empty or main project code)
├── invoicepipe.code-workspace  # VS Code workspace config
└── ...                         # Other files and folders
```

## 🚀 Quick Start Guide

### 👋 New to InvoicePipe? Start Here!

**Complete Beginner?** 
- 📚 **[Step-by-Step Assignment: Building a Simple Invoice CLI Tool](docs/preparation-work/step-by-step-assignment.md)** - Perfect for learning the basics

**Ready to Build?** Choose your path:

#### 🔧 Option 1: Simple CLI Tool (Recommended)
1. 📖 **[Using QuantaLogic PyZerox to Analyze PDFs and Images](docs/using-quantalogic-pyzerox.md)** - Core functionality
2. ⚙️ **[Managing Environment Variables and Configuration](docs/managing-env-files.md)** - Essential setup

#### 🚀 Option 2: Full FastAPI Application
1. 🏗️ **[Setting Up a FastAPI Project with Modern Python Tooling](docs/setup-fastapi-project.md)** - Project structure
2. 📋 **[InvoicePipe Specification](docs/spec-invoice.md)** - Requirements and API design
3. ⚙️ **[Managing Environment Variables and Configuration](docs/managing-env-files.md)** - Configuration setup

### 🧠 Advanced Features (Optional)
- 🎯 **[Instructor Library Integration Guide](docs/instructor-integration-guide.md)** - Structured data extraction
- 🌐 **[LiteLLM Integration Guide](docs/litellm-integration-guide.md)** - Universal LLM gateway and cost management

### 🛠️ Development Tools
- 🔧 **[Git & GitHub CLI Cheat Sheet](docs/git-github-cheat-sheet.md)** - GitHub Flow workflow and commands

### 📋 Prerequisites
- Python 3.11
- API key for a supported vision model (OpenAI, Gemini, Claude, etc.)
- System tools for PDF/image processing (detailed in setup guides)

---

For more information on supported models, file types, and advanced options, refer to the [QuantaLogic PyZerox documentation](https://github.com/quantalogic/quantalogic-pyzerox).
