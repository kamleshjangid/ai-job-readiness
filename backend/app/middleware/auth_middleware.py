"""
Authentication Middleware

This middleware handles JWT token validation, expiration checking,
and provides appropriate error responses for authentication issues.

@author AI Job Readiness Team
@version 1.0.0
"""

import logging
from typing import Callable, Optional
from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from app.utils.jwt_utils import JWTTokenManager, handle_token_error, validate_token_expiration
from app.utils.response import create_error_response

logger = logging.getLogger(__name__)


class JWTAuthMiddleware(BaseHTTPMiddleware):
    """
    JWT Authentication Middleware
    
    This middleware validates JWT tokens and handles token expiration
    for protected routes.
    """
    
    def __init__(self, app, excluded_paths: Optional[list] = None):
        super().__init__(app)
        self.excluded_paths = excluded_paths or [
            "/",
            "/health",
            "/docs",
            "/redoc",
            "/openapi.json",
            "/api/v1/auth/register",
            "/api/v1/auth/jwt/login",
            "/api/v1/auth/jwt/refresh",
            "/api/v1/info",
            "/api/v1/performance",
            "/api/v1/cache/status"
        ]
    
    async def dispatch(self, request: Request, call_next: Callable):
        """
        Process the request and validate JWT tokens for protected routes.
        
        Args:
            request: The incoming HTTP request
            call_next: The next middleware/handler in the chain
            
        Returns:
            Response: HTTP response
        """
        # Skip authentication for excluded paths
        if self._should_skip_auth(request.url.path):
            return await call_next(request)
        
        # Extract token from Authorization header
        token = self._extract_token(request)
        
        if not token:
            return handle_token_error("missing")
        
        # Validate token
        if not self._validate_token(token):
            return handle_token_error("invalid")
        
        # Check token expiration
        if not validate_token_expiration(token):
            return handle_token_error("expired")
        
        # Add user info to request state for use in route handlers
        payload = JWTTokenManager.verify_access_token(token)
        if payload:
            request.state.user_id = payload.get("sub")
            request.state.token_payload = payload
        
        return await call_next(request)
    
    def _should_skip_auth(self, path: str) -> bool:
        """
        Check if the path should skip authentication.
        
        Args:
            path: The request path
            
        Returns:
            bool: True if path should skip auth, False otherwise
        """
        # Check exact matches
        if path in self.excluded_paths:
            return True
        
        # Check if path starts with any excluded path
        for excluded_path in self.excluded_paths:
            if path.startswith(excluded_path):
                return True
        
        return False
    
    def _extract_token(self, request: Request) -> Optional[str]:
        """
        Extract JWT token from Authorization header.
        
        Args:
            request: The HTTP request
            
        Returns:
            Optional[str]: The JWT token if found, None otherwise
        """
        authorization = request.headers.get("Authorization")
        
        if not authorization:
            return None
        
        try:
            scheme, token = authorization.split(" ", 1)
            if scheme.lower() != "bearer":
                logger.warning(f"Invalid authorization scheme: {scheme}")
                return None
            
            return token
        except ValueError:
            logger.warning("Malformed authorization header")
            return None
    
    def _validate_token(self, token: str) -> bool:
        """
        Validate the JWT token structure and signature.
        
        Args:
            token: The JWT token to validate
            
        Returns:
            bool: True if token is valid, False otherwise
        """
        try:
            payload = JWTTokenManager.verify_access_token(token)
            return payload is not None
        except Exception as e:
            logger.error(f"Token validation error: {e}")
            return False


class TokenExpirationHandler:
    """
    Handler for token expiration scenarios.
    """
    
    @staticmethod
    def create_expired_token_response() -> JSONResponse:
        """
        Create a standardized response for expired tokens.
        
        Returns:
            JSONResponse: Error response for expired token
        """
        return create_error_response(
            message="Access token has expired. Please re-authenticate.",
            error="token_expired",
            status_code=status.HTTP_401_UNAUTHORIZED,
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    @staticmethod
    def create_invalid_token_response() -> JSONResponse:
        """
        Create a standardized response for invalid tokens.
        
        Returns:
            JSONResponse: Error response for invalid token
        """
        return create_error_response(
            message="Invalid access token. Please re-authenticate.",
            error="token_invalid",
            status_code=status.HTTP_401_UNAUTHORIZED,
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    @staticmethod
    def create_missing_token_response() -> JSONResponse:
        """
        Create a standardized response for missing tokens.
        
        Returns:
            JSONResponse: Error response for missing token
        """
        return create_error_response(
            message="Access token is required. Please provide a valid token.",
            error="token_missing",
            status_code=status.HTTP_401_UNAUTHORIZED,
            headers={"WWW-Authenticate": "Bearer"}
        )


def get_current_user_id(request: Request) -> str:
    """
    Get the current user ID from the request state.
    
    Args:
        request: The HTTP request
        
    Returns:
        str: The user ID
        
    Raises:
        HTTPException: If user ID is not found in request state
    """
    user_id = getattr(request.state, "user_id", None)
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not authenticated"
        )
    return user_id


def get_token_payload(request: Request) -> dict:
    """
    Get the token payload from the request state.
    
    Args:
        request: The HTTP request
        
    Returns:
        dict: The token payload
        
    Raises:
        HTTPException: If token payload is not found in request state
    """
    payload = getattr(request.state, "token_payload", None)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token payload not found"
        )
    return payload
