"""
JWT Token Management Utilities

This module provides utilities for JWT token management, including
token creation, validation, expiration handling, and refresh functionality.

@author AI Job Readiness Team
@version 1.0.0
"""

import jwt
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, Tuple
from fastapi import HTTPException, status
from fastapi.responses import JSONResponse

from app.core.config import settings
from app.utils.response import create_error_response
import logging

logger = logging.getLogger(__name__)


class JWTTokenManager:
    """JWT Token management utility class"""
    
    @staticmethod
    def create_access_token(subject: str, expires_delta: Optional[timedelta] = None) -> str:
        """
        Create a JWT access token with 1-hour expiration.
        
        Args:
            subject: The subject (usually user ID) to encode in the token
            expires_delta: Optional custom expiration time delta
            
        Returns:
            str: Encoded JWT access token
            
        Raises:
            HTTPException: If token creation fails
        """
        try:
            if expires_delta:
                expire = datetime.utcnow() + expires_delta
            else:
                # Default to 1 hour expiration
                expire = datetime.utcnow() + timedelta(
                    minutes=settings.security.access_token_expire_minutes
                )
            
            to_encode = {
                "exp": expire,
                "sub": str(subject),
                "type": "access",
                "iat": datetime.utcnow()
            }
            
            encoded_jwt = jwt.encode(
                to_encode, 
                settings.security.secret_key, 
                algorithm=settings.security.algorithm
            )
            
            logger.debug(f"Access token created for subject: {subject}, expires: {expire}")
            return encoded_jwt
            
        except Exception as e:
            logger.error(f"Failed to create access token: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create access token"
            )
    
    @staticmethod
    def create_refresh_token(subject: str) -> str:
        """
        Create a JWT refresh token with 7-day expiration.
        
        Args:
            subject: The subject (usually user ID) to encode in the token
            
        Returns:
            str: Encoded JWT refresh token
            
        Raises:
            HTTPException: If token creation fails
        """
        try:
            expire = datetime.utcnow() + timedelta(
                days=settings.security.refresh_token_expire_days
            )
            
            to_encode = {
                "exp": expire,
                "sub": str(subject),
                "type": "refresh",
                "iat": datetime.utcnow()
            }
            
            encoded_jwt = jwt.encode(
                to_encode, 
                settings.security.users_secret, 
                algorithm=settings.security.algorithm
            )
            
            logger.debug(f"Refresh token created for subject: {subject}, expires: {expire}")
            return encoded_jwt
            
        except Exception as e:
            logger.error(f"Failed to create refresh token: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create refresh token"
            )
    
    @staticmethod
    def verify_access_token(token: str) -> Optional[Dict[str, Any]]:
        """
        Verify and decode an access token.
        
        Args:
            token: The JWT access token to verify
            
        Returns:
            Optional[Dict[str, Any]]: Token payload if valid, None if invalid/expired
        """
        try:
            payload = jwt.decode(
                token, 
                settings.security.secret_key, 
                algorithms=[settings.security.algorithm]
            )
            
            # Verify token type
            if payload.get("type") != "access":
                logger.warning("Invalid token type for access token")
                return None
                
            return payload
            
        except jwt.ExpiredSignatureError:
            logger.warning("Access token has expired")
            return None
        except jwt.InvalidTokenError as e:
            logger.warning(f"Invalid access token: {e}")
            return None
        except Exception as e:
            logger.error(f"Error verifying access token: {e}")
            return None
    
    @staticmethod
    def verify_refresh_token(token: str) -> Optional[Dict[str, Any]]:
        """
        Verify and decode a refresh token.
        
        Args:
            token: The JWT refresh token to verify
            
        Returns:
            Optional[Dict[str, Any]]: Token payload if valid, None if invalid/expired
        """
        try:
            payload = jwt.decode(
                token, 
                settings.security.users_secret, 
                algorithms=[settings.security.algorithm]
            )
            
            # Verify token type
            if payload.get("type") != "refresh":
                logger.warning("Invalid token type for refresh token")
                return None
                
            return payload
            
        except jwt.ExpiredSignatureError:
            logger.warning("Refresh token has expired")
            return None
        except jwt.InvalidTokenError as e:
            logger.warning(f"Invalid refresh token: {e}")
            return None
        except Exception as e:
            logger.error(f"Error verifying refresh token: {e}")
            return None
    
    @staticmethod
    def get_token_expiration(token: str) -> Optional[datetime]:
        """
        Get the expiration time of a token without verifying it.
        
        Args:
            token: The JWT token
            
        Returns:
            Optional[datetime]: Expiration time if token is valid, None otherwise
        """
        try:
            # Decode without verification to get expiration
            payload = jwt.decode(token, options={"verify_signature": False})
            exp_timestamp = payload.get("exp")
            if exp_timestamp:
                return datetime.fromtimestamp(exp_timestamp)
            return None
        except Exception as e:
            logger.error(f"Error getting token expiration: {e}")
            return None
    
    @staticmethod
    def is_token_expired(token: str) -> bool:
        """
        Check if a token is expired.
        
        Args:
            token: The JWT token to check
            
        Returns:
            bool: True if token is expired, False otherwise
        """
        try:
            exp_time = JWTTokenManager.get_token_expiration(token)
            if exp_time:
                return datetime.utcnow() >= exp_time
            return True
        except Exception as e:
            logger.error(f"Error checking token expiration: {e}")
            return True
    
    @staticmethod
    def get_token_remaining_time(token: str) -> Optional[timedelta]:
        """
        Get the remaining time until token expiration.
        
        Args:
            token: The JWT token
            
        Returns:
            Optional[timedelta]: Remaining time until expiration, None if invalid
        """
        try:
            exp_time = JWTTokenManager.get_token_expiration(token)
            if exp_time:
                remaining = exp_time - datetime.utcnow()
                return remaining if remaining.total_seconds() > 0 else timedelta(0)
            return None
        except Exception as e:
            logger.error(f"Error getting token remaining time: {e}")
            return None


def create_token_pair(user_id: str) -> Tuple[str, str]:
    """
    Create both access and refresh tokens for a user.
    
    Args:
        user_id: The user ID
        
    Returns:
        Tuple[str, str]: (access_token, refresh_token)
    """
    access_token = JWTTokenManager.create_access_token(user_id)
    refresh_token = JWTTokenManager.create_refresh_token(user_id)
    return access_token, refresh_token


def handle_token_error(error_type: str, message: str = None) -> JSONResponse:
    """
    Handle token-related errors with appropriate HTTP responses.
    
    Args:
        error_type: Type of token error
        message: Custom error message
        
    Returns:
        JSONResponse: Appropriate error response
    """
    error_messages = {
        "expired": "Access token has expired. Please re-authenticate.",
        "invalid": "Invalid access token. Please re-authenticate.",
        "missing": "Access token is required. Please provide a valid token.",
        "malformed": "Malformed access token. Please re-authenticate.",
        "refresh_expired": "Refresh token has expired. Please login again.",
        "refresh_invalid": "Invalid refresh token. Please login again."
    }
    
    error_message = message or error_messages.get(error_type, "Authentication error")
    
    if error_type in ["expired", "refresh_expired"]:
        return create_error_response(
            message=error_message,
            errors=[error_type],
            status_code=status.HTTP_401_UNAUTHORIZED
        )
    elif error_type in ["invalid", "malformed", "refresh_invalid"]:
        return create_error_response(
            message=error_message,
            errors=[error_type],
            status_code=status.HTTP_401_UNAUTHORIZED
        )
    elif error_type == "missing":
        return create_error_response(
            message=error_message,
            errors=[error_type],
            status_code=status.HTTP_401_UNAUTHORIZED
        )
    else:
        return create_error_response(
            message=error_message,
            errors=[error_type],
            status_code=status.HTTP_401_UNAUTHORIZED
        )


def validate_token_expiration(token: str) -> bool:
    """
    Validate that a token is not expired and provide detailed logging.
    
    Args:
        token: The JWT token to validate
        
    Returns:
        bool: True if token is valid and not expired, False otherwise
    """
    try:
        if JWTTokenManager.is_token_expired(token):
            logger.warning("Token validation failed: Token has expired")
            return False
        
        remaining_time = JWTTokenManager.get_token_remaining_time(token)
        if remaining_time:
            logger.debug(f"Token is valid, remaining time: {remaining_time}")
        
        return True
        
    except Exception as e:
        logger.error(f"Token validation error: {e}")
        return False
