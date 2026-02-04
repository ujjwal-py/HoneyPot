"""
Persona Engine - Manages persona selection and characteristics
"""

import json
import random
from pathlib import Path
from typing import Dict, Optional


class PersonaEngine:
    """Manages AI agent personas"""
    
    def __init__(self):
        self.personas = {}
        self.load_personas()
    
    def load_personas(self):
        """Load all persona JSON files"""
        personas_dir = Path(__file__).parent.parent / "personas"
        
        if not personas_dir.exists():
            raise FileNotFoundError(f"Personas directory not found: {personas_dir}")
        
        for persona_file in personas_dir.glob("*.json"):
            with open(persona_file, 'r', encoding='utf-8') as f:
                persona_data = json.load(f)
                persona_name = persona_data["name"]
                self.personas[persona_name] = persona_data
        
        print(f"✅ Loaded {len(self.personas)} personas: {list(self.personas.keys())}")
    
    def select_persona(self, scam_type: str = None, message: str = None) -> Dict:
        """
        Select appropriate persona based on scam type
        
        Matching logic:
        - Urgent/Authority scams → Ramesh Uncle (trusts authority)
        - Work/Time pressure → Priya (busy professional)
        - Money-making schemes → Rahul (desperate student)
        - Default → Random selection
        """
        
        if scam_type:
            scam_type_lower = scam_type.lower()
            
            # Authority/urgency scams target elderly
            if any(x in scam_type_lower for x in ['impersonation', 'urgent_action', 'refund']):
                return self.personas.get("Ramesh Kumar")
            
            # Investment/crypto scams target students
            elif any(x in scam_type_lower for x in ['crypto', 'investment', 'earn']):
                return self.personas.get("Rahul Verma")
            
            # Generic/prize scams target busy professionals
            elif any(x in scam_type_lower for x in ['prize', 'upi_collection']):
                return self.personas.get("Priya Sharma")
        
        # Message-based selection
        if message:
            message_lower = message.lower()
            
            if any(word in message_lower for word in ['bank', 'pension', 'account block', 'sir', 'madam']):
                return self.personas.get("Ramesh Kumar")
            
            if any(word in message_lower for word in ['earn', 'money', 'crypto', 'investment', 'bro']):
                return self.personas.get("Rahul Verma")
            
            if any(word in message_lower for word in ['urgent', 'meeting', 'work', 'professional']):
                return self.personas.get("Priya Sharma")
        
        # Random selection as fallback
        return random.choice(list(self.personas.values()))
    
    def get_persona_by_name(self, name: str) -> Optional[Dict]:
        """Get specific persona by name"""
        return self.personas.get(name)
    
    def get_all_personas(self) -> Dict[str, Dict]:
        """Get all available personas"""
        return self.personas


# Global persona engine instance
persona_engine = PersonaEngine()
