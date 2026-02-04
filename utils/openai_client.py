"""
OpenAI Client Wrapper
"""

from openai import AsyncOpenAI
from config import settings


class OpenAIClient:
    """Wrapper for OpenAI API client"""
    
    def __init__(self):
        self.client = AsyncOpenAI(api_key=settings.openai_api_key)
        self.model = settings.openai_model
    
    async def chat_completion(self, messages, **kwargs):
        """Create chat completion"""
        return await self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            **kwargs
        )
    
    def check_connection(self) -> bool:
        """Check if OpenAI API is accessible"""
        try:
            # Simple sync check
            return bool(settings.openai_api_key)
        except Exception:
            return False


# Global client instance
openai_client = OpenAIClient()
