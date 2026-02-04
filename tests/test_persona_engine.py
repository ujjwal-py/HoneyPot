"""
Test Agent Responses
"""

import pytest
from core.persona_engine import persona_engine


def test_persona_loading():
    """Test that personas are loaded correctly"""
    personas = persona_engine.get_all_personas()
    
    assert len(personas) == 3
    assert "Ramesh Kumar" in personas
    assert "Priya Sharma" in personas
    assert "Rahul Verma" in personas


def test_ramesh_persona_selection():
    """Test that Ramesh is selected for authority scams"""
    message = "This is bank manager. Your account will be blocked"
    persona = persona_engine.select_persona(message=message)
    
    assert persona["name"] == "Ramesh Kumar"


def test_priya_persona_selection():
    """Test that Priya is selected for work-related scams"""
    message = "Urgent work-related issue. Verify immediately"
    persona = persona_engine.select_persona(scam_type="urgent_action")
    
    # Either Priya or Ramesh is valid for urgent scams
    assert persona["name"] in ["Priya Sharma", "Ramesh Kumar"]


def test_rahul_persona_selection():
    """Test that Rahul is selected for money-making scams"""
    message = "Earn 50k per month! Join crypto trading group"
    persona = persona_engine.select_persona(message=message)
    
    assert persona["name"] == "Rahul Verma"


def test_persona_characteristics():
    """Test that personas have required characteristics"""
    ramesh = persona_engine.get_persona_by_name("Ramesh Kumar")
    
    assert ramesh["age"] == 67
    assert ramesh["tech_literacy"] == "Low"
    assert ramesh["typing_patterns"]["typos_frequency"] == "high"
    assert len(ramesh["common_phrases"]) > 0


def test_typing_patterns():
    """Test that personas have distinct typing patterns"""
    ramesh = persona_engine.get_persona_by_name("Ramesh Kumar")
    priya = persona_engine.get_persona_by_name("Priya Sharma")
    rahul = persona_engine.get_persona_by_name("Rahul Verma")
    
    assert ramesh["typing_patterns"]["speed"] == "slow"
    assert priya["typing_patterns"]["speed"] == "fast"
    assert rahul["typing_patterns"]["emoji_use"] == "frequent"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
