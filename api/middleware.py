"""
API Middleware - Rate limiting and authentication
"""

import time
from collections import defaultdict
from typing import Dict
from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware

from config import settings


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Rate limiting middleware"""
    
    def __init__(self, app):
        super().__init__(app)
        self.request_counts: Dict[str, list] = defaultdict(list)
    
    async def dispatch(self, request: Request, call_next):
        # Get session ID from request
        session_id = None
        
        if request.method == "POST":
            # Try to get session ID from body
            body = await request.body()
            request._body = body  # Save for later use
            
            try:
                import json
                data = json.loads(body)
                session_id = data.get("sessionId")
            except:
                pass
        
        # Apply rate limiting if session ID present
        if session_id:
            if not self._check_rate_limit(session_id):
                raise HTTPException(
                    status_code=429,
                    detail="Rate limit exceeded. Max 30 requests per minute per session."
                )
        
        response = await call_next(request)
        return response
    
    def _check_rate_limit(self, session_id: str) -> bool:
        """Check if request is within rate limit"""
        now = time.time()
        window = settings.rate_limit_window
        max_requests = settings.rate_limit_requests
        
        # Clean old requests
        self.request_counts[session_id] = [
            req_time for req_time in self.request_counts[session_id]
            if now - req_time < window
        ]
        
        # Check limit
        if len(self.request_counts[session_id]) >= max_requests:
            return False
        
        # Add current request
        self.request_counts[session_id].append(now)
        return True
