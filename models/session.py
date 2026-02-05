"""
Session and Intelligence Models
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Union
from datetime import datetime


class MessageContent(BaseModel):
    sender: str
    text: str
    timestamp: Union[str, int, float]


class MessageMetadata(BaseModel):
    channel: Optional[str] = "SMS"
    language: Optional[str] = "English"
    locale: Optional[str] = "IN"


class ConversationMessage(BaseModel):
    sender: str
    text: str
    timestamp: Union[str, int, float]


class MessageRequest(BaseModel):
    sessionId: str
    message: MessageContent
    conversationHistory: List[ConversationMessage] = Field(default_factory=list)
    metadata: Optional[MessageMetadata] = None


class EngagementMetrics(BaseModel):
    engagementDurationSeconds: int
    totalMessagesExchanged: int


class ExtractedIntelligence(BaseModel):
    bankAccounts: List[str] = Field(default_factory=list)
    upiIds: List[str] = Field(default_factory=list)
    phishingLinks: List[str] = Field(default_factory=list)
    phoneNumbers: List[str] = Field(default_factory=list)
    suspiciousKeywords: List[str] = Field(default_factory=list)


class MessageResponse(BaseModel):
    status: str
    reply: str
    scamDetected: bool = False
    engagementMetrics: Optional[EngagementMetrics] = None
    extractedIntelligence: Optional[ExtractedIntelligence] = None
    agentNotes: Optional[str] = None


class DetailedMessageResponse(BaseModel):
    sessionId: str
    reply: str
    scamDetected: bool
    scamIntents: List[str]
    confidence: float
    shouldContinue: bool
    extractedIntelligence: Dict
    conversationPhase: str
    messageCount: int
