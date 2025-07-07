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
