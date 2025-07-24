"""
Slug generation utilities
"""

import re
import unicodedata
from typing import Optional


def create_slug(text: str, max_length: Optional[int] = 50) -> str:
    """
    Create a URL-friendly slug from text
    
    Args:
        text: Input text to convert to slug
        max_length: Maximum length of the slug
    
    Returns:
        URL-friendly slug
    """
    # Normalize unicode characters
    text = unicodedata.normalize('NFKD', text)
    
    # Convert to lowercase
    text = text.lower()
    
    # Replace Polish characters
    polish_chars = {
        'ą': 'a', 'ć': 'c', 'ę': 'e', 'ł': 'l', 'ń': 'n',
        'ó': 'o', 'ś': 's', 'ź': 'z', 'ż': 'z'
    }
    
    for polish, latin in polish_chars.items():
        text = text.replace(polish, latin)
    
    # Remove non-alphanumeric characters except spaces and hyphens
    text = re.sub(r'[^\w\s-]', '', text)
    
    # Replace spaces and multiple hyphens with single hyphen
    text = re.sub(r'[-\s]+', '-', text)
    
    # Remove leading/trailing hyphens
    text = text.strip('-')
    
    # Truncate if necessary
    if max_length and len(text) > max_length:
        text = text[:max_length].rstrip('-')
    
    return text
