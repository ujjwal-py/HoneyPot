"""
Test Scam Detection Module
"""

import pytest
from core.scam_detector import scam_detector
from tests.mock_scam_scenarios import MOCK_SCAM_CONVERSATIONS, LEGITIMATE_MESSAGES


def test_fake_prize_detection():
    """Test detection of fake prize scams"""
    message = "Congratulations! You have won Rs 50,000 in lucky draw"
    result = scam_detector.detect_scam_intent(message)
    
    assert result["is_scam"] == True
    assert result["confidence"] >= 0.6
    assert "fake_prize" in result["scam_types"]


def test_bank_impersonation_detection():
    """Test detection of bank impersonation scams"""
    message = "This is State Bank customer care. Your account will be blocked within 24 hours"
    result = scam_detector.detect_scam_intent(message)
    
    assert result["is_scam"] == True
    assert "impersonation" in result["scam_types"] or "urgent_action" in result["scam_types"]


def test_upi_collection_detection():
    """Test detection of UPI collection scams"""
    message = "Send your UPI ID to receive money: test@paytm"
    result = scam_detector.detect_scam_intent(message)
    
    assert result["is_scam"] == True
    assert "upi_collection_scam" in result["scam_types"]


def test_crypto_investment_detection():
    """Test detection of crypto investment scams"""
    message = "Guaranteed 300% returns in Bitcoin trading! Join now!"
    result = scam_detector.detect_scam_intent(message)
    
    assert result["is_scam"] == True
    assert "crypto_investment" in result["scam_types"]


def test_refund_scam_detection():
    """Test detection of refund scams"""
    message = "Your payment failed. Click here for refund: https://bit.ly/refund"
    result = scam_detector.detect_scam_intent(message)
    
    assert result["is_scam"] == True
    assert "refund_scam" in result["scam_types"]


def test_remote_access_detection():
    """Test detection of remote access scams"""
    message = "Download AnyDesk for technical support"
    result = scam_detector.detect_scam_intent(message)
    
    assert result["is_scam"] == True
    assert "remote_access" in result["scam_types"]


def test_legitimate_messages():
    """Test that legitimate messages are not flagged as scams"""
    for message in LEGITIMATE_MESSAGES:
        result = scam_detector.detect_scam_intent(message)
        assert result["is_scam"] == False, f"False positive for: {message}"


def test_urgency_detection():
    """Test urgency level detection"""
    urgent_msg = "Act now! Your account will be blocked immediately!"
    result = scam_detector.detect_scam_intent(urgent_msg)
    
    assert result["urgency_level"] == "high"


def test_multiple_patterns():
    """Test detection when multiple scam patterns present"""
    message = "Urgent! You won Rs 1 lakh! Send UPI ID to claim prize immediately!"
    result = scam_detector.detect_scam_intent(message)
    
    assert result["is_scam"] == True
    assert result["confidence"] >= 0.8
    assert len(result["scam_types"]) >= 2


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
