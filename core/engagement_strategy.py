"""
Engagement Strategy - Controls conversation flow and engagement tactics
"""

import time
from enum import Enum
from typing import Dict


class EngagementPhase(Enum):
    """Conversation engagement phases"""
    INITIATED = "initiated"           # First contact
    SCAM_SUSPECTED = "scam_suspected" # Detection triggered
    ENGAGING = "engaging"             # Active conversation
    EXTRACTING = "extracting"         # Gathering intelligence
    PROLONGING = "prolonging"         # Keeping scammer engaged
    COMPLETED = "completed"           # Exit conditions met
    SUSPICIOUS = "suspicious"         # Scammer may be detecting


class ConversationState:
    """Manages conversation state and engagement strategy"""
    
    def __init__(self, session_id: str, persona: Dict):
        self.session_id = session_id
        self.persona = persona
        self.phase = EngagementPhase.INITIATED
        self.message_count = 0
        self.intelligence_extracted = {
            "upi_ids": [],
            "phone_numbers": [],
            "urls": [],
            "bank_accounts": [],
            "ifsc_codes": []
        }
        self.scammer_tactics = []
        self.scam_types = []
        self.engagement_start_time = time.time()
        self.last_message_time = time.time()
        self.scam_confirmed = False
        self.scam_confidence = 0.0
        self.conversation_history = []
        self.callback_sent = False
    
    def should_continue_engagement(self) -> bool:
        """Decide if agent should continue engaging"""
        
        # Exit conditions
        if self.message_count > 20:  # Max conversation length
            return False
        
        if self.phase == EngagementPhase.COMPLETED:
            return False
        
        # Check if sufficient intelligence gathered
        intel_count = self._count_intelligence()
        if intel_count >= 3:  # Got at least 3 pieces of intelligence
            if self.message_count >= 10:  # And had reasonable conversation
                return False
        
        # Check if scammer went silent (2 hours)
        silence_duration = time.time() - self.last_message_time
        if silence_duration > 7200:
            return False
        
        return True
    
    def update_phase(self, latest_message: str, scam_confidence: float):
        """Update engagement phase based on conversation state"""
        
        if self.phase == EngagementPhase.INITIATED:
            if scam_confidence > 0.6:
                self.phase = EngagementPhase.SCAM_SUSPECTED
        
        elif self.phase == EngagementPhase.SCAM_SUSPECTED:
            if self.message_count >= 3:
                self.phase = EngagementPhase.ENGAGING
        
        elif self.phase == EngagementPhase.ENGAGING:
            intel_count = self._count_intelligence()
            if intel_count > 0:
                self.phase = EngagementPhase.EXTRACTING
        
        elif self.phase == EngagementPhase.EXTRACTING:
            if self.message_count >= 10:
                self.phase = EngagementPhase.PROLONGING
        
        # Check if scammer is getting suspicious
        suspicion_keywords = ["are you real", "bot", "ai", "fake", "testing you"]
        if any(kw in latest_message.lower() for kw in suspicion_keywords):
            self.phase = EngagementPhase.SUSPICIOUS
    
    def update_intelligence(self, new_intelligence: Dict):
        """Add newly extracted intelligence to session"""
        for key in self.intelligence_extracted.keys():
            if key in new_intelligence:
                self.intelligence_extracted[key].extend(new_intelligence[key])
                # De-duplicate
                self.intelligence_extracted[key] = list(set(self.intelligence_extracted[key]))
    
    def _count_intelligence(self) -> int:
        """Count total intelligence items"""
        return sum(len(v) for v in self.intelligence_extracted.values())
    
    def get_engagement_metrics(self) -> Dict:
        """Get engagement statistics"""
        duration = time.time() - self.engagement_start_time
        intel_count = self._count_intelligence()
        
        return {
            "duration_seconds": int(duration),
            "message_count": self.message_count,
            "intelligence_count": intel_count,
            "phase": self.phase.value,
            "scam_confidence": self.scam_confidence
        }
    
    def to_dict(self) -> Dict:
        """Convert state to dictionary for storage"""
        return {
            "session_id": self.session_id,
            "persona": self.persona,
            "phase": self.phase.value,
            "message_count": self.message_count,
            "intelligence_extracted": self.intelligence_extracted,
            "scammer_tactics": self.scammer_tactics,
            "scam_types": self.scam_types,
            "engagement_start_time": self.engagement_start_time,
            "last_message_time": self.last_message_time,
            "scam_confirmed": self.scam_confirmed,
            "scam_confidence": self.scam_confidence,
            "conversation_history": self.conversation_history,
            "callback_sent": self.callback_sent
        }
