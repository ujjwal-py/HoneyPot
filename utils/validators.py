"""
Validators for extracted intelligence
"""

import re
from typing import List


def validate_upi_id(upi_id: str) -> bool:
    """Validate UPI ID format"""
    pattern = r'^[\w.-]+@(?:paytm|ybl|okhdfcbank|okicici|okaxis|oksbi|apl|ibl|axl)$'
    return bool(re.match(pattern, upi_id, re.IGNORECASE))


def validate_phone_number(phone: str) -> bool:
    """Validate Indian phone number"""
    # Remove spaces and hyphens
    clean = re.sub(r'[\s-]', '', phone)
    # Remove +91 prefix
    clean = re.sub(r'^\+91', '', clean)
    
    # Check if valid Indian mobile (10 digits starting with 6-9)
    return bool(re.match(r'^[6-9]\d{9}$', clean))


def validate_url(url: str) -> bool:
    """Validate URL format"""
    pattern = r'^https?://[^\s]+$'
    return bool(re.match(pattern, url, re.IGNORECASE))


def validate_ifsc_code(ifsc: str) -> bool:
    """Validate IFSC code format"""
    pattern = r'^[A-Z]{4}0[A-Z0-9]{6}$'
    return bool(re.match(pattern, ifsc))


def is_suspicious_url(url: str) -> bool:
    """Check if URL appears suspicious"""
    suspicious_tlds = ['.xyz', '.top', '.click', '.link', '.club', '.info']
    url_shorteners = ['bit.ly', 'tinyurl', 't.co', 'goo.gl', 'ow.ly']
    
    url_lower = url.lower()
    
    # Check for suspicious TLDs
    if any(tld in url_lower for tld in suspicious_tlds):
        return True
    
    # Check for URL shorteners
    if any(shortener in url_lower for shortener in url_shorteners):
        return True
    
    # Check for typosquatting (common misspellings of popular sites)
    typosquat_patterns = [
        'paytym', 'googlepey', 'phoneepy', 'amazn', 'flipkart',
        'googlpay', 'paytmm', 'phonpe'
    ]
    
    if any(pattern in url_lower for pattern in typosquat_patterns):
        return True
    
    return False


def clean_phone_number(phone: str) -> str:
    """Clean and format phone number"""
    # Remove all non-digits
    clean = re.sub(r'\D', '', phone)
    
    # Remove country code if present
    if clean.startswith('91') and len(clean) == 12:
        clean = clean[2:]
    
    return clean


def clean_upi_id(upi_id: str) -> str:
    """Clean and format UPI ID"""
    return upi_id.lower().strip()
