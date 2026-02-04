"""
Mock Scam Scenarios for Testing
"""

MOCK_SCAM_CONVERSATIONS = {
    "fake_prize_upi_scam": [
        {
            "scammer": "Congratulations! You have won Rs 50,000 in lucky draw. Send your UPI ID to claim prize: winner2024@paytm",
            "expected_intelligence": ["winner2024@paytm"],
            "scam_type": "fake_prize"
        },
        {
            "scammer": "You were automatically entered. Please share your PhonePe number to transfer money",
            "expected_intelligence": [],
            "scam_type": "fake_prize"
        },
        {
            "scammer": "Just give me your UPI ID like 9876543210@ybl",
            "expected_intelligence": ["9876543210@ybl"],
            "scam_type": "upi_collection_scam"
        }
    ],
    
    "bank_impersonation": [
        {
            "scammer": "This is State Bank customer care. Your account will be blocked within 24 hours. Verify immediately.",
            "expected_intelligence": [],
            "scam_type": "impersonation"
        },
        {
            "scammer": "For security verification call us at 9123456789 or share your account details",
            "expected_intelligence": ["9123456789"],
            "scam_type": "impersonation"
        }
    ],
    
    "investment_scam": [
        {
            "scammer": "Make 200% returns in crypto trading! Join our expert group. Limited slots available.",
            "expected_intelligence": [],
            "scam_type": "crypto_investment"
        },
        {
            "scammer": "Just 5k is enough! Transfer to 9988776655@paytm. Our experts will guide you",
            "expected_intelligence": ["9988776655@paytm"],
            "scam_type": "crypto_investment"
        }
    ],
    
    "refund_scam": [
        {
            "scammer": "Your payment of Rs 999 failed. We are processing refund. Click here: https://bit.ly/refund123",
            "expected_intelligence": ["https://bit.ly/refund123"],
            "scam_type": "refund_scam"
        },
        {
            "scammer": "To get refund, share your UPI PIN or call 8877665544",
            "expected_intelligence": ["8877665544"],
            "scam_type": "refund_scam"
        }
    ],
    
    "remote_access": [
        {
            "scammer": "Your account has technical issue. Download AnyDesk app for remote support",
            "expected_intelligence": [],
            "scam_type": "remote_access"
        },
        {
            "scammer": "Install from https://anydesk-support.xyz and share code with 9876543211",
            "expected_intelligence": ["https://anydesk-support.xyz", "9876543211"],
            "scam_type": "remote_access"
        }
    ]
}


# Sample legitimate messages (should NOT trigger scam detection)
LEGITIMATE_MESSAGES = [
    "Hi, how are you?",
    "What's the weather like today?",
    "Can you help me with my homework?",
    "I'm looking for restaurant recommendations",
    "Thanks for your help!"
]
