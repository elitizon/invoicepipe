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
