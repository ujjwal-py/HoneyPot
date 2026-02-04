"""
Session and Intelligence Models
"""

from pydantic import BaseModel
from typing import List, Optional, Dict
from datetime import datetime


class MessageRequest(BaseModel):
    """Request model for honeypot endpoint"""
    sessionId: str
    message: str


class MessageResponse(BaseModel):
    """Response model for honeypot endpoint"""
    status: str
    reply: str


class IntelligenceData(BaseModel):
    """Intelligence extracted from conversation"""
    upi_ids: List[str] = []
    phone_numbers: List[str] = []
    urls: List[str] = []
    bank_accounts: List[str] = []
    ifsc_codes: List[str] = []
    suspicious_keywords: List[str] = []


class SessionData(BaseModel):
    """Complete session data"""
    session_id: str
    persona_name: str
    scam_confirmed: bool = False
    scam_confidence: float = 0.0
    scam_types: List[str] = []
    message_count: int = 0
    intelligence_extracted: IntelligenceData = IntelligenceData()
    phase: str = "initiated"
    callback_sent: bool = False
    created_at: datetime = datetime.now()
    last_active: datetime = datetime.now()


class DetailedMessageResponse(BaseModel):
    """Detailed response for testing/debugging"""
    sessionId: str
    reply: str
    scamDetected: bool
    scamIntents: List[str]
    confidence: float
    shouldContinue: bool
    extractedIntelligence: Dict
    conversationPhase: str
    messageCount: int


class CallbackPayload(BaseModel):
    """Payload sent to GUVI callback endpoint"""
    sessionId: str
    scamDetected: bool
    totalMessagesExchanged: int
    extractedIntelligence: Dict
    agentNotes: str
    engagementMetrics: Dict
