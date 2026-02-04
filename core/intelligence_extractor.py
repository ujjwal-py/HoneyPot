"""
Intelligence Extraction Module - Extracts actionable intelligence from conversations
"""

import re
from typing import Dict, List


# UPI ID Patterns
UPI_PATTERNS = [
    r'\b[\w.-]+@(?:paytm|ybl|okhdfcbank|okicici|okaxis|oksbi|apl|ibl|axl)\b',
    r'\b\d{10}@(?:paytm|ybl|okhdfcbank|okicici|okaxis|oksbi)\b',
]

# Indian Phone Numbers
PHONE_PATTERNS = [
    r'\+91[\s-]?\d{10}',
    r'\b[6-9]\d{9}\b',  # Indian mobile numbers start with 6-9
    r'\b0\d{2,4}[\s-]?\d{6,8}\b'  # Landlines
]

# URLs
URL_PATTERNS = [
    r'https?://[^\s]+',
    r'bit\.ly/[^\s]+',
    r'tinyurl\.com/[^\s]+',
]

# Bank Account Numbers
BANK_ACCOUNT_PATTERNS = [
    r'\b\d{9,18}\b',
    r'A/C\s*:?\s*\d{9,18}',
    r'Account\s*(?:Number|No\.?)?\s*:?\s*\d{9,18}'
]

# IFSC Codes
IFSC_PATTERNS = [
    r'\b[A-Z]{4}0[A-Z0-9]{6}\b'
]


class IntelligenceExtractor:
    """Extract and validate intelligence from scam messages"""
    
    def __init__(self):
        pass
    
    def extract_intelligence(self, message: str, conversation_history: List = None) -> Dict:
        """
        Extract and validate intelligence from messages
        
        Returns:
        {
            "upi_ids": [],
            "phone_numbers": [],
            "urls": [],
            "bank_accounts": [],
            "ifsc_codes": [],
            "suspicious_keywords": []
        }
        """
        
        intelligence = {
            "upi_ids": [],
            "phone_numbers": [],
            "urls": [],
            "bank_accounts": [],
            "ifsc_codes": [],
            "suspicious_keywords": []
        }
        
        # Extract UPI IDs
        for pattern in UPI_PATTERNS:
            matches = re.findall(pattern, message, re.IGNORECASE)
            intelligence["upi_ids"].extend(matches)
        
        # Extract phone numbers
        for pattern in PHONE_PATTERNS:
            matches = re.findall(pattern, message)
            intelligence["phone_numbers"].extend(matches)
        
        # Extract URLs
        for pattern in URL_PATTERNS:
            matches = re.findall(pattern, message, re.IGNORECASE)
            intelligence["urls"].extend(matches)
        
        # Extract bank accounts (be careful - avoid false positives)
        if 'account' in message.lower() or 'a/c' in message.lower():
            for pattern in BANK_ACCOUNT_PATTERNS:
                matches = re.findall(pattern, message, re.IGNORECASE)
                intelligence["bank_accounts"].extend(matches)
        
        # Extract IFSC codes
        for pattern in IFSC_PATTERNS:
            matches = re.findall(pattern, message)
            intelligence["ifsc_codes"].extend(matches)
        
        # Extract suspicious keywords
        intelligence["suspicious_keywords"] = self._extract_keywords(message)
        
        # Validate extracted data
        intelligence["upi_ids"] = self.validate_upi_ids(intelligence["upi_ids"])
        intelligence["phone_numbers"] = self.validate_phone_numbers(intelligence["phone_numbers"])
        intelligence["urls"] = self.validate_urls(intelligence["urls"])
        
        # De-duplicate
        for key in intelligence:
            if isinstance(intelligence[key], list):
                intelligence[key] = list(set(intelligence[key]))
        
        return intelligence
    
    def validate_upi_ids(self, upi_ids: List[str]) -> List[str]:
        """Validate UPI ID format and provider"""
        valid_providers = [
            'paytm', 'ybl', 'okhdfcbank', 'okicici', 'okaxis', 
            'oksbi', 'apl', 'ibl', 'axl'
        ]
        
        validated = []
        for upi_id in upi_ids:
            provider = upi_id.split('@')[-1].lower()
            if any(prov in provider for prov in valid_providers):
                validated.append(upi_id.lower())
        
        return validated
    
    def validate_phone_numbers(self, phones: List[str]) -> List[str]:
        """Validate Indian phone number format"""
        validated = []
        for phone in phones:
            # Remove spaces, hyphens
            clean = re.sub(r'[\s-]', '', phone)
            # Remove +91 prefix if present
            clean = re.sub(r'^\+91', '', clean)
            
            # Check if valid Indian number (10 digits starting with 6-9)
            if re.match(r'^[6-9]\d{9}$', clean):
                validated.append(clean)
        
        return validated
    
    def validate_urls(self, urls: List[str]) -> List[str]:
        """Check if URLs are potentially malicious"""
        validated = []
        
        # Suspicious TLDs
        suspicious_tlds = ['.xyz', '.top', '.click', '.link', '.club', '.info']
        
        # URL shorteners
        url_shorteners = ['bit.ly', 'tinyurl', 't.co', 'goo.gl', 'ow.ly']
        
        for url in urls:
            # Check for suspicious TLDs
            if any(tld in url.lower() for tld in suspicious_tlds):
                validated.append(url)
                continue
            
            # Check for URL shorteners (likely phishing)
            if any(shortener in url.lower() for shortener in url_shorteners):
                validated.append(url)
                continue
            
            # Add all URLs for now
            validated.append(url)
        
        return validated
    
    def _extract_keywords(self, message: str) -> List[str]:
        """Extract suspicious keywords from message"""
        suspicious_keywords = [
            'urgent', 'verify', 'blocked', 'expired', 'confirm',
            'prize', 'won', 'claim', 'otp', 'pin', 'password',
            'bank', 'account', 'transfer', 'payment'
        ]
        
        found_keywords = []
        message_lower = message.lower()
        
        for keyword in suspicious_keywords:
            if keyword in message_lower:
                found_keywords.append(keyword)
        
        return found_keywords
    
    def aggregate_intelligence(self, session_intelligence: Dict) -> int:
        """Count total intelligence items extracted"""
        count = 0
        for key in ['upi_ids', 'phone_numbers', 'urls', 'bank_accounts', 'ifsc_codes']:
            count += len(session_intelligence.get(key, []))
        return count


# Global extractor instance
intelligence_extractor = IntelligenceExtractor()
