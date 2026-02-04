"""
GUVI Callback Handler - Sends intelligence reports to hackathon endpoint
"""

import aiohttp
import time
from typing import Dict, List
from config import settings


async def send_guvi_callback(session: Dict) -> Dict:
    """
    Send final intelligence report to GUVI endpoint
    
    Triggered when:
    - Sufficient intelligence extracted (2+ items)
    - Reasonable engagement duration (8+ messages)
    - Conversation naturally ended
    """
    
    callback_payload = {
        "sessionId": session["session_id"],
        "scamDetected": session["scam_confirmed"],
        "totalMessagesExchanged": session["message_count"],
        "extractedIntelligence": {
            "bankAccounts": session["intelligence_extracted"]["bank_accounts"],
            "upiIds": session["intelligence_extracted"]["upi_ids"],
            "phishingLinks": session["intelligence_extracted"]["urls"],
            "phoneNumbers": session["intelligence_extracted"]["phone_numbers"],
            "suspiciousKeywords": extract_keywords_from_history(
                session["conversation_history"]
            )
        },
        "agentNotes": generate_agent_notes(session),
        "engagementMetrics": {
            "durationSeconds": calculate_duration(session),
            "intelligenceDensity": calculate_intelligence_density(session),
            "scamTypes": list(set(session["scam_types"])),
            "personaUsed": session["persona"]["name"]
        }
    }
    
    try:
        async with aiohttp.ClientSession() as http_session:
            async with http_session.post(
                settings.guvi_callback_url,
                json=callback_payload,
                headers={"Content-Type": "application/json"},
                timeout=aiohttp.ClientTimeout(total=10)
            ) as response:
                if response.status == 200:
                    print(f"✅ Callback successful for session {session['session_id']}")
                    result = await response.json()
                    return result
                else:
                    print(f"❌ Callback failed: {response.status}")
                    error_text = await response.text()
                    print(f"Error: {error_text}")
                    return None
    
    except Exception as e:
        print(f"❌ Callback error: {str(e)}")
        return None


def should_trigger_callback(session: Dict) -> bool:
    """Determine if callback should be sent"""
    
    # Minimum requirements
    if session["message_count"] < settings.callback_min_messages:
        return False
    
    # Check intelligence count
    intel_count = sum(
        len(v) for v in session["intelligence_extracted"].values()
        if isinstance(v, list)
    )
    if intel_count < settings.min_intelligence_count:
        return False
    
    # Check if already sent
    if session.get("callback_sent", False):
        return False
    
    # Trigger if significant intelligence gathered
    if intel_count >= 5 and session["message_count"] >= 12:
        return True
    
    # Check if conversation is winding down
    # (This would check the engagement state in real implementation)
    if session["message_count"] >= 15:
        return True
    
    return False


def extract_keywords_from_history(conversation_history: List[Dict]) -> List[str]:
    """Extract all suspicious keywords from conversation"""
    
    keywords = set()
    suspicious_words = [
        'urgent', 'verify', 'blocked', 'expired', 'confirm',
        'prize', 'won', 'claim', 'otp', 'pin', 'password',
        'bank', 'account', 'transfer', 'payment', 'upi'
    ]
    
    for msg in conversation_history:
        if msg["role"] == "user":  # Only from scammer
            content_lower = msg["content"].lower()
            for word in suspicious_words:
                if word in content_lower:
                    keywords.add(word)
    
    return list(keywords)


def generate_agent_notes(session: Dict) -> str:
    """Generate summary notes about the engagement"""
    
    persona_name = session["persona"]["name"]
    scam_types = ", ".join(session["scam_types"]) if session["scam_types"] else "unknown"
    intel_count = sum(
        len(v) for v in session["intelligence_extracted"].values()
        if isinstance(v, list)
    )
    
    notes = f"Persona '{persona_name}' engaged with suspected {scam_types} scam. "
    notes += f"Successfully extracted {intel_count} intelligence items over "
    notes += f"{session['message_count']} message exchanges. "
    notes += f"Scam confidence: {session['scam_confidence']:.0%}."
    
    return notes


def calculate_duration(session: Dict) -> int:
    """Calculate engagement duration in seconds"""
    start_time = session.get("engagement_start_time", time.time())
    return int(time.time() - start_time)


def calculate_intelligence_density(session: Dict) -> float:
    """Calculate intelligence items per message"""
    intel_count = sum(
        len(v) for v in session["intelligence_extracted"].values()
        if isinstance(v, list)
    )
    
    if session["message_count"] == 0:
        return 0.0
    
    return round(intel_count / session["message_count"], 2)
