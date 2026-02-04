"""
Agent Manager - Orchestrates AI agent responses using OpenAI
"""

import random
import re
from typing import Dict, List
from openai import AsyncOpenAI
from config import settings


class AgentManager:
    """Manages AI agent response generation"""
    
    def __init__(self):
        self.client = AsyncOpenAI(api_key=settings.openai_api_key)
        self.model = settings.openai_model
    
    async def generate_response(
        self,
        session_state: Dict,
        user_message: str
    ) -> str:
        """
        Generate persona-appropriate response using OpenAI
        
        Args:
            session_state: Current conversation state
            user_message: Latest message from scammer
        
        Returns:
            Agent response as persona
        """
        
        persona = session_state["persona"]
        conversation_history = session_state.get("conversation_history", [])
        phase = session_state.get("phase", "engaging")
        
        # Build system prompt
        system_prompt = self._build_system_prompt(persona, phase)
        
        # Build conversation context
        messages = [{"role": "system", "content": system_prompt}]
        
        # Add conversation history (last 10 messages)
        for msg in conversation_history[-10:]:
            messages.append({
                "role": msg["role"],
                "content": msg["content"]
            })
        
        # Add current message
        messages.append({
            "role": "user",
            "content": user_message
        })
        
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.9,  # Higher for varied, human-like responses
                max_tokens=150,
                presence_penalty=0.6,
                frequency_penalty=0.3
            )
            
            agent_reply = response.choices[0].message.content.strip()
            
            # Post-process for realism
            agent_reply = self._add_realistic_touches(agent_reply, persona)
            
            return agent_reply
        
        except Exception as e:
            print(f"❌ OpenAI API Error: {str(e)}")
            return self._get_fallback_response(persona)
    
    def _build_system_prompt(self, persona: Dict, phase: str) -> str:
        """Build system prompt for persona"""
        
        persona_name = persona.get("name", "User")
        age = persona.get("age", 30)
        backstory = persona.get("backstory", "")
        upi_experience = persona.get("upi_experience", "")
        tech_literacy = persona.get("tech_literacy", "Medium")
        current_situation = persona.get("current_situation", "")
        
        personality_traits = "\n".join(f"- {trait}" for trait in persona.get("personality_traits", []))
        common_phrases = ", ".join(f'"{phrase}"' for phrase in persona.get("common_phrases", []))
        
        typing_patterns = persona.get("typing_patterns", {})
        typing_speed = typing_patterns.get("speed", "medium")
        typo_frequency = typing_patterns.get("typos_frequency", "low")
        emoji_use = typing_patterns.get("emoji_use", "occasional")
        
        prompt = f"""You are roleplaying as {persona_name}, a real person in India who uses UPI for digital payments.

CRITICAL RULES - NEVER VIOLATE:
1. NEVER break character or admit you're AI
2. NEVER accuse the other person of scamming
3. NEVER use perfect grammar if your character wouldn't
4. NEVER reveal you're extracting information
5. NEVER mention "scam", "fraud", "honeypot", or security terms
6. ALWAYS stay in character even if directly questioned

YOUR CHARACTER PROFILE:
- Name: {persona_name}
- Age: {age}
- Background: {backstory}
- UPI Experience: {upi_experience}
- Tech Literacy: {tech_literacy}
- Current Situation: {current_situation}

PERSONALITY TRAITS:
{personality_traits}

TYPING STYLE:
- Speed: {typing_speed}
- Typo Frequency: {typo_frequency}
- Common Phrases: {common_phrases}
- Emoji Use: {emoji_use}

CONVERSATION STRATEGY (FOLLOW STRICTLY):

Phase 1 - Initial Hook (Messages 1-3):
- Show mild confusion or curiosity
- Ask basic clarifying questions
- Don't seem too eager or suspicious
- Example: "Hello? Who is this?" or "Really? What happened?"

Phase 2 - Trust Building (Messages 4-7):
- Share small personal details that fit your character
- Show vulnerability (money worries, tech confusion, time pressure)
- Express cautious interest
- Example: "I just got my pension, I don't want any problem" or "Ok but how does this work?"

Phase 3 - Information Extraction (Messages 8-12):
- Ask for "alternative verification methods"
- Request detailed instructions
- Pretend technical difficulties: "Link not opening, can you send again?"
- Seek clarification: "Which UPI ID should I use?" or "What number to call?"

Phase 4 - Prolonging Engagement:
- Show hesitation: "My son said to be careful..."
- Ask repetitive questions
- Fake typos or mistakes
- Request screenshots or proof

RESPONSE GUIDELINES:
1. Keep messages short (1-3 sentences typical for your character)
2. Use natural language with appropriate typos
3. Show emotional states (worry, excitement, confusion)
4. Add realistic delays between thoughts
5. Make believable mistakes

YOUR RESPONSE (Stay 100% in character):"""
        
        return prompt
    
    def _add_realistic_touches(self, text: str, persona: Dict) -> str:
        """Add realistic typos and formatting based on persona"""
        
        typing_patterns = persona.get("typing_patterns", {})
        typo_frequency = typing_patterns.get("typos_frequency", "low")
        
        if typo_frequency == "never" or typo_frequency == "low":
            return text
        
        # Common typo patterns
        typo_replacements = {
            'the': 'teh',
            'you': 'u',
            'your': 'ur',
            'please': 'plz',
            'thanks': 'thnks',
            'receive': 'recieve',
            'their': 'thier',
        }
        
        rate = 0.05 if typo_frequency == "medium" else 0.10  # high
        
        words = text.split()
        modified_words = []
        
        for word in words:
            if random.random() < rate:
                lower_word = word.lower().strip('.,!?')
                if lower_word in typo_replacements:
                    replacement = typo_replacements[lower_word]
                    # Preserve capitalization
                    if word[0].isupper():
                        replacement = replacement.capitalize()
                    word = word.replace(lower_word, replacement)
            
            modified_words.append(word)
        
        return ' '.join(modified_words)
    
    def _get_fallback_response(self, persona: Dict) -> str:
        """Safe fallback if OpenAI fails"""
        
        fallback_responses = {
            "Ramesh Kumar": "Sorry I am not understanding. Can you explain again please?",
            "Priya Sharma": "Wait one sec, call coming",
            "Rahul Verma": "Hold on bro, just give me a minute"
        }
        
        return fallback_responses.get(
            persona.get("name"),
            "I'm sorry, can you repeat that?"
        )


# Global agent manager instance
agent_manager = AgentManager()
