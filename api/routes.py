"""
API Routes - Main honeypot endpoints
"""

import time
import asyncio
from typing import Dict
from fastapi import APIRouter, Header, HTTPException

from models.session import MessageRequest, MessageResponse, DetailedMessageResponse
from core import (
    scam_detector,
    persona_engine,
    intelligence_extractor,
    agent_manager,
    ConversationState
)
from utils import send_guvi_callback, should_trigger_callback
from config import settings


router = APIRouter()

# In-memory session storage (use Redis in production)
active_sessions: Dict[str, Dict] = {}


@router.post("/api/honeypot", response_model=MessageResponse)
async def honeypot_endpoint(
    request: MessageRequest,
    x_api_key: str = Header(...)
):
    """
    PRIMARY HACKATHON ENDPOINT
    
    Receives scam messages and returns agent responses.
    Returns: {"status": "success", "reply": "agent response"}
    """
    
    # Validate API key
    if x_api_key != settings.api_key:
        raise HTTPException(status_code=401, detail="Invalid API key")
    
    session_id = request.sessionId
    message = request.message
    
    # Get or create session
    if session_id not in active_sessions:
        active_sessions[session_id] = initialize_session(session_id, message)
    
    session = active_sessions[session_id]
    
    # Step 1: Detect scam intent
    scam_detection = scam_detector.detect_scam_intent(message)
    
    # Step 2: If scam detected, activate agent
    if scam_detection["is_scam"]:
        # Update session state
        session["scam_confirmed"] = True
        session["scam_confidence"] = scam_detection["confidence"]
        session["scam_types"].extend(scam_detection["scam_types"])
        
        # Generate agent response
        agent_response = await agent_manager.generate_response(
            session_state=session,
            user_message=message
        )
        
        # Step 3: Extract intelligence
        extracted = intelligence_extractor.extract_intelligence(
            message,
            session["conversation_history"]
        )
        
        # Update session intelligence
        for key in session["intelligence_extracted"].keys():
            if key in extracted and isinstance(extracted[key], list):
                session["intelligence_extracted"][key].extend(extracted[key])
                # De-duplicate
                session["intelligence_extracted"][key] = list(
                    set(session["intelligence_extracted"][key])
                )
        
        # Step 4: Update conversation history
        session["conversation_history"].append({
            "role": "user",
            "content": message,
            "timestamp": time.time()
        })
        session["conversation_history"].append({
            "role": "assistant",
            "content": agent_response,
            "timestamp": time.time()
        })
        session["message_count"] += 1
        session["last_message_time"] = time.time()
        
        # Step 5: Check if should trigger callback
        if should_trigger_callback(session):
            session["callback_sent"] = True
            asyncio.create_task(send_guvi_callback(session))
        
        return MessageResponse(status="success", reply=agent_response)
    
    else:
        # Not a scam - generic response
        return MessageResponse(
            status="success",
            reply="Thank you for your message."
        )


@router.post("/api/v1/message", response_model=DetailedMessageResponse)
async def detailed_message_endpoint(
    request: MessageRequest,
    x_api_key: str = Header(...)
):
    """
    INTERNAL TESTING ENDPOINT
    
    Returns full diagnostic information for development and debugging.
    NOT used for hackathon evaluation.
    """
    
    # Validate API key
    if x_api_key != settings.api_key:
        raise HTTPException(status_code=401, detail="Invalid API key")
    
    session_id = request.sessionId
    message = request.message
    
    # Get or create session
    if session_id not in active_sessions:
        active_sessions[session_id] = initialize_session(session_id, message)
    
    session = active_sessions[session_id]
    
    # Detect scam
    scam_detection = scam_detector.detect_scam_intent(message)
    
    # Generate response if scam
    if scam_detection["is_scam"]:
        session["scam_confirmed"] = True
        session["scam_confidence"] = scam_detection["confidence"]
        
        agent_response = await agent_manager.generate_response(
            session_state=session,
            user_message=message
        )
        
        # Extract intelligence
        extracted = intelligence_extractor.extract_intelligence(
            message,
            session["conversation_history"]
        )
        
        # Update session
        for key in session["intelligence_extracted"].keys():
            if key in extracted and isinstance(extracted[key], list):
                session["intelligence_extracted"][key].extend(extracted[key])
                session["intelligence_extracted"][key] = list(
                    set(session["intelligence_extracted"][key])
                )
        
        session["conversation_history"].append({
            "role": "user",
            "content": message,
            "timestamp": time.time()
        })
        session["conversation_history"].append({
            "role": "assistant",
            "content": agent_response,
            "timestamp": time.time()
        })
        session["message_count"] += 1
        
        return DetailedMessageResponse(
            sessionId=session_id,
            reply=agent_response,
            scamDetected=True,
            scamIntents=scam_detection["scam_types"],
            confidence=scam_detection["confidence"],
            shouldContinue=session["message_count"] < settings.max_conversation_length,
            extractedIntelligence=session["intelligence_extracted"],
            conversationPhase=session.get("phase", "engaging"),
            messageCount=session["message_count"]
        )
    else:
        return DetailedMessageResponse(
            sessionId=session_id,
            reply="Thank you for your message.",
            scamDetected=False,
            scamIntents=[],
            confidence=scam_detection["confidence"],
            shouldContinue=False,
            extractedIntelligence={},
            conversationPhase="none",
            messageCount=0
        )


@router.get("/api/honeypot")
async def honeypot_get():
    """GET endpoint for GUVI tester compatibility"""
    return {
        "status": "success",
        "message": "Agentic Honeypot API is running",
        "version": "1.0.0"
    }


@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": time.time(),
        "active_sessions": len(active_sessions),
        "openai_configured": bool(settings.openai_api_key)
    }


def initialize_session(session_id: str, first_message: str) -> Dict:
    """Initialize a new conversation session"""
    
    # Select appropriate persona based on message
    persona = persona_engine.select_persona(message=first_message)
    
    session = {
        "session_id": session_id,
        "persona": persona,
        "phase": "initiated",
        "message_count": 0,
        "intelligence_extracted": {
            "upi_ids": [],
            "phone_numbers": [],
            "urls": [],
            "bank_accounts": [],
            "ifsc_codes": []
        },
        "scammer_tactics": [],
        "scam_types": [],
        "engagement_start_time": time.time(),
        "last_message_time": time.time(),
        "scam_confirmed": False,
        "scam_confidence": 0.0,
        "conversation_history": [],
        "callback_sent": False
    }
    
    return session
