"""
Scam Detection Engine - Hybrid approach combining rule-based and ML-based detection
"""

import re
from typing import Dict, List
from enum import Enum


class ScamType(Enum):
    """Types of scam patterns detected"""
    URGENT_ACTION = "urgent_action"
    FAKE_PRIZE = "fake_prize"
    IMPERSONATION = "impersonation"
    UPI_COLLECTION = "upi_collection_scam"
    REFUND_SCAM = "refund_scam"
    REMOTE_ACCESS = "remote_access"
    CRYPTO_INVESTMENT = "crypto_investment"
    NONE = "none"


# Scam Pattern Database (Based on 2025 UPI Fraud Research)
SCAM_PATTERNS = {
    "urgent_action": {
        "keywords": [
            "urgent", "immediately", "within 24 hours", "account will be blocked",
            "verify now", "confirm details", "update kyc", "expired", "suspended",
            "last chance", "act now", "today only", "limited time"
        ],
        "weight": 0.7
    },
    "fake_prize": {
        "keywords": [
            "congratulations", "won", "prize", "lottery", "lucky draw",
            "claim now", "winner", "₹", "lakh", "reward", "crore",
            "selected", "free gift", "bonus"
        ],
        "weight": 0.8
    },
    "impersonation": {
        "keywords": [
            "bank manager", "rbi", "npci", "customer care", "support team",
            "verify your account", "we need", "provide your", "confirm your",
            "official", "department", "government", "authority"
        ],
        "weight": 0.75
    },
    "upi_collection_scam": {
        "keywords": [
            "send upi id", "paytm number", "gpay id", "phonepe id",
            "receive money", "transfer to", "payment link", "qr code",
            "upi pin", "payment details", "account number"
        ],
        "weight": 0.85
    },
    "refund_scam": {
        "keywords": [
            "refund", "cashback", "reverse transaction", "return amount",
            "processing refund", "click here", "enter pin", "otp",
            "wrong transaction", "failed payment", "money back"
        ],
        "weight": 0.8
    },
    "remote_access": {
        "keywords": [
            "anydesk", "teamviewer", "quicksupport", "screen share",
            "download app", "install", "remote access", "technical issue",
            "screen sharing", "remote support", "take control"
        ],
        "weight": 0.9
    },
    "crypto_investment": {
        "keywords": [
            "investment opportunity", "guaranteed returns", "crypto", "bitcoin",
            "forex trading", "stock tips", "10x returns", "expert advice",
            "trading", "profit", "earn money", "make money fast"
        ],
        "weight": 0.75
    }
}


class ScamDetector:
    """Hybrid scam detection engine"""
    
    def __init__(self):
        self.patterns = SCAM_PATTERNS
    
    def detect_scam_intent(self, message: str) -> Dict:
        """
        Detect scam patterns in message
        
        Returns:
        {
            "is_scam": bool,
            "confidence": float,
            "detected_patterns": list,
            "scam_types": list,
            "urgency_level": str,
            "red_flags": list
        }
        """
        message_lower = message.lower()
        
        detected_patterns = []
        pattern_scores = []
        scam_types = []
        red_flags = []
        
        # Rule-based pattern matching
        for pattern_name, pattern_data in self.patterns.items():
            keywords = pattern_data["keywords"]
            weight = pattern_data["weight"]
            
            matches = []
            for keyword in keywords:
                if keyword.lower() in message_lower:
                    matches.append(keyword)
            
            if matches:
                detected_patterns.append(pattern_name)
                pattern_scores.append(weight)
                scam_types.append(pattern_name)
                red_flags.extend(matches)
        
        # Calculate overall confidence
        if pattern_scores:
            confidence = min(max(pattern_scores) + (len(pattern_scores) * 0.05), 1.0)
        else:
            confidence = 0.0
        
        # Determine urgency level
        urgency_level = self._determine_urgency(message_lower)
        
        # Additional heuristics
        if self._check_suspicious_urls(message):
            confidence = min(confidence + 0.15, 1.0)
            red_flags.append("suspicious_url")
        
        if self._check_upi_pattern(message):
            confidence = min(confidence + 0.2, 1.0)
            red_flags.append("upi_id_request")
        
        if self._check_phone_pattern(message):
            confidence = min(confidence + 0.1, 1.0)
            red_flags.append("phone_number_present")
        
        # Decision threshold
        is_scam = confidence >= 0.6
        
        return {
            "is_scam": is_scam,
            "confidence": round(confidence, 2),
            "detected_patterns": list(set(detected_patterns)),
            "scam_types": list(set(scam_types)),
            "urgency_level": urgency_level,
            "red_flags": list(set(red_flags))
        }
    
    def _determine_urgency(self, message: str) -> str:
        """Determine urgency level of message"""
        high_urgency = [
            "immediately", "urgent", "now", "today", "within 24",
            "last chance", "expire", "block", "suspend"
        ]
        medium_urgency = [
            "soon", "quick", "fast", "asap", "hurry"
        ]
        
        if any(word in message for word in high_urgency):
            return "high"
        elif any(word in message for word in medium_urgency):
            return "medium"
        else:
            return "low"
    
    def _check_suspicious_urls(self, message: str) -> bool:
        """Check for suspicious URLs"""
        url_pattern = r'https?://[^\s]+'
        urls = re.findall(url_pattern, message)
        
        if not urls:
            return False
        
        suspicious_tlds = ['.xyz', '.top', '.click', '.link', '.club', '.info']
        url_shorteners = ['bit.ly', 'tinyurl', 't.co', 'goo.gl']
        
        for url in urls:
            if any(tld in url.lower() for tld in suspicious_tlds):
                return True
            if any(shortener in url.lower() for shortener in url_shorteners):
                return True
        
        return False
    
    def _check_upi_pattern(self, message: str) -> bool:
        """Check for UPI ID patterns"""
        upi_pattern = r'\b[\w.-]+@(?:paytm|ybl|okhdfcbank|okicici|okaxis|oksbi|apl|ibl|axl)\b'
        return bool(re.search(upi_pattern, message, re.IGNORECASE))
    
    def _check_phone_pattern(self, message: str) -> bool:
        """Check for phone number patterns"""
        phone_pattern = r'\b[6-9]\d{9}\b|\+91[\s-]?\d{10}'
        return bool(re.search(phone_pattern, message))


# Global detector instance
scam_detector = ScamDetector()
