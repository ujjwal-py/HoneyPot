"""
Core package initialization
"""

from .scam_detector import scam_detector, ScamDetector
from .persona_engine import persona_engine, PersonaEngine
from .intelligence_extractor import intelligence_extractor, IntelligenceExtractor
from .engagement_strategy import ConversationState, EngagementPhase
from .agent_manager import agent_manager, AgentManager

__all__ = [
    'scam_detector',
    'ScamDetector',
    'persona_engine',
    'PersonaEngine',
    'intelligence_extractor',
    'IntelligenceExtractor',
    'ConversationState',
    'EngagementPhase',
    'agent_manager',
    'AgentManager'
]
