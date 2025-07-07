"""Data models for invoice processing."""

from datetime import date as _date
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
    date: Optional[_date] = None
    due_date: Optional[_date] = None
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
