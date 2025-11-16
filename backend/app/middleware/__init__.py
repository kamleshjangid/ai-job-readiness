"""
Middleware package for AI Job Readiness Platform

This package contains middleware components for authentication,
logging, and other cross-cutting concerns.

@author AI Job Readiness Team
@version 1.0.0
"""

from .auth_middleware import (
    JWTAuthMiddleware,
    TokenExpirationHandler,
    get_current_user_id,
    get_token_payload
)

__all__ = [
    "JWTAuthMiddleware",
    "TokenExpirationHandler", 
    "get_current_user_id",
    "get_token_payload"
]
