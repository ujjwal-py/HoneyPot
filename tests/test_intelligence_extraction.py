"""
Test Intelligence Extraction Module
"""

import pytest
from core.intelligence_extractor import intelligence_extractor


def test_upi_id_extraction():
    """Test UPI ID extraction"""
    message = "Send money to test123@paytm or backup456@ybl"
    result = intelligence_extractor.extract_intelligence(message)
    
    assert "test123@paytm" in result["upi_ids"]
    assert "backup456@ybl" in result["upi_ids"]


def test_phone_number_extraction():
    """Test phone number extraction"""
    message = "Call me at 9876543210 or +91 8765432109"
    result = intelligence_extractor.extract_intelligence(message)
    
    assert "9876543210" in result["phone_numbers"]
    assert "8765432109" in result["phone_numbers"]


def test_url_extraction():
    """Test URL extraction"""
    message = "Click here: https://bit.ly/scam123 or visit http://fake-bank.xyz"
    result = intelligence_extractor.extract_intelligence(message)
    
    assert len(result["urls"]) == 2
    assert any("bit.ly" in url for url in result["urls"])


def test_ifsc_extraction():
    """Test IFSC code extraction"""
    message = "Transfer to account SBIN0001234"
    result = intelligence_extractor.extract_intelligence(message)
    
    assert "SBIN0001234" in result["ifsc_codes"]


def test_keyword_extraction():
    """Test suspicious keyword extraction"""
    message = "Urgent! Verify your account. Click link to claim prize"
    result = intelligence_extractor.extract_intelligence(message)
    
    keywords = result["suspicious_keywords"]
    assert "urgent" in keywords
    assert "verify" in keywords
    assert "claim" in keywords


def test_upi_validation():
    """Test UPI ID validation"""
    valid_upis = ["test@paytm", "user123@ybl", "9876543210@paytm"]
    invalid_upis = ["test@gmail", "user@unknown", "invalid"]
    
    validated = intelligence_extractor.validate_upi_ids(valid_upis + invalid_upis)
    
    for upi in valid_upis:
        assert upi.lower() in validated
    
    for upi in invalid_upis:
        assert upi not in validated


def test_phone_validation():
    """Test phone number validation"""
    valid_phones = ["9876543210", "+919876543210", "8765432109"]
    invalid_phones = ["1234567890", "123", "+1234567890"]
    
    validated = intelligence_extractor.validate_phone_numbers(valid_phones + invalid_phones)
    
    assert "9876543210" in validated
    assert "8765432109" in validated
    assert "1234567890" not in validated


def test_no_false_positives():
    """Test that normal messages don't extract false intelligence"""
    message = "Hello, how are you doing today?"
    result = intelligence_extractor.extract_intelligence(message)
    
    assert len(result["upi_ids"]) == 0
    assert len(result["phone_numbers"]) == 0
    assert len(result["urls"]) == 0


def test_deduplication():
    """Test that duplicate intelligence is removed"""
    message = "Send to test@paytm or test@paytm again"
    result = intelligence_extractor.extract_intelligence(message)
    
    assert len(result["upi_ids"]) == 1


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
