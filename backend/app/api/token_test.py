"""
Token Testing Endpoints

This module provides endpoints for testing JWT token functionality,
including token creation, validation, and expiration testing.

@author AI Job Readiness Team
@version 1.0.0
"""

from datetime import datetime, timedelta
from typing import Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.responses import JSONResponse

from app.utils.jwt_utils import (
    JWTTokenManager, 
    create_token_pair, 
    validate_token_expiration,
    handle_token_error
)
from app.utils.response import create_success_response, create_error_response
from app.middleware.auth_middleware import get_current_user_id, get_token_payload

router = APIRouter()


@router.get("/token/info", tags=["Token Testing"])
async def get_token_info(request: Request) -> JSONResponse:
    """
    Get information about the current access token.
    
    This endpoint demonstrates token expiration and remaining time.
    
    Returns:
        JSONResponse: Token information including expiration details
    """
    try:
        # Extract token from Authorization header
        authorization = request.headers.get("Authorization")
        if not authorization:
            return handle_token_error("missing")
        
        token = authorization.split(" ", 1)[1] if " " in authorization else None
        if not token:
            return handle_token_error("malformed")
        
        # Get token payload
        payload = JWTTokenManager.verify_access_token(token)
        if not payload:
            return handle_token_error("invalid")
        
        # Check if token is expired
        is_expired = JWTTokenManager.is_token_expired(token)
        if is_expired:
            return handle_token_error("expired")
        
        # Get token details
        exp_time = JWTTokenManager.get_token_expiration(token)
        remaining_time = JWTTokenManager.get_token_remaining_time(token)
        
        token_info = {
            "user_id": payload.get("sub"),
            "token_type": payload.get("type"),
            "issued_at": datetime.fromtimestamp(payload.get("iat", 0)).isoformat() if payload.get("iat") else None,
            "expires_at": exp_time.isoformat() if exp_time else None,
            "is_expired": is_expired,
            "remaining_seconds": int(remaining_time.total_seconds()) if remaining_time else 0,
            "remaining_minutes": round(remaining_time.total_seconds() / 60, 2) if remaining_time else 0,
            "expires_in_hours": round(remaining_time.total_seconds() / 3600, 2) if remaining_time else 0
        }
        
        return create_success_response(
            message="Token information retrieved successfully",
            data=token_info
        )
        
    except Exception as e:
        return create_error_response(
            message="Failed to get token information",
            errors=[str(e)],
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@router.post("/token/test-expiration", tags=["Token Testing"])
async def test_token_expiration(request: Request) -> JSONResponse:
    """
    Test token expiration by creating a short-lived token.
    
    This endpoint creates a token that expires in 1 minute for testing purposes.
    
    Returns:
        JSONResponse: Test token information
    """
    try:
        # Get current user ID
        user_id = get_current_user_id(request)
        
        # Create a test token that expires in 1 minute
        test_token = JWTTokenManager.create_access_token(
            user_id, 
            expires_delta=timedelta(minutes=1)
        )
        
        # Get token details
        exp_time = JWTTokenManager.get_token_expiration(test_token)
        remaining_time = JWTTokenManager.get_token_remaining_time(test_token)
        
        test_info = {
            "test_token": test_token,
            "user_id": user_id,
            "expires_at": exp_time.isoformat() if exp_time else None,
            "expires_in_minutes": 1,
            "remaining_seconds": int(remaining_time.total_seconds()) if remaining_time else 0,
            "note": "This token will expire in 1 minute for testing purposes"
        }
        
        return create_success_response(
            message="Test token created successfully",
            data=test_info
        )
        
    except Exception as e:
        return create_error_response(
            message="Failed to create test token",
            errors=[str(e)],
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@router.get("/token/validate", tags=["Token Testing"])
async def validate_current_token(request: Request) -> JSONResponse:
    """
    Validate the current access token and return validation results.
    
    Returns:
        JSONResponse: Token validation results
    """
    try:
        # Extract token from Authorization header
        authorization = request.headers.get("Authorization")
        if not authorization:
            return handle_token_error("missing")
        
        token = authorization.split(" ", 1)[1] if " " in authorization else None
        if not token:
            return handle_token_error("malformed")
        
        # Validate token
        is_valid = validate_token_expiration(token)
        payload = JWTTokenManager.verify_access_token(token)
        is_expired = JWTTokenManager.is_token_expired(token)
        remaining_time = JWTTokenManager.get_token_remaining_time(token)
        
        validation_result = {
            "is_valid": is_valid and payload is not None,
            "is_expired": is_expired,
            "user_id": payload.get("sub") if payload else None,
            "token_type": payload.get("type") if payload else None,
            "remaining_seconds": int(remaining_time.total_seconds()) if remaining_time else 0,
            "validation_timestamp": datetime.utcnow().isoformat()
        }
        
        if is_valid and payload:
            return create_success_response(
                message="Token is valid",
                data=validation_result
            )
        else:
            return create_error_response(
                message="Token validation failed",
                errors=["invalid_token"],
                status_code=status.HTTP_401_UNAUTHORIZED,
                meta={"validation_result": validation_result}
            )
        
    except Exception as e:
        return create_error_response(
            message="Token validation error",
            errors=[str(e)],
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@router.get("/token/expiration-status", tags=["Token Testing"])
async def get_expiration_status(request: Request) -> JSONResponse:
    """
    Get detailed expiration status of the current token.
    
    Returns:
        JSONResponse: Detailed expiration status
    """
    try:
        # Extract token from Authorization header
        authorization = request.headers.get("Authorization")
        if not authorization:
            return handle_token_error("missing")
        
        token = authorization.split(" ", 1)[1] if " " in authorization else None
        if not token:
            return handle_token_error("malformed")
        
        # Get detailed expiration information
        exp_time = JWTTokenManager.get_token_expiration(token)
        remaining_time = JWTTokenManager.get_token_remaining_time(token)
        is_expired = JWTTokenManager.is_token_expired(token)
        
        current_time = datetime.utcnow()
        
        expiration_status = {
            "current_time": current_time.isoformat(),
            "expiration_time": exp_time.isoformat() if exp_time else None,
            "is_expired": is_expired,
            "remaining_time": {
                "total_seconds": int(remaining_time.total_seconds()) if remaining_time else 0,
                "minutes": round(remaining_time.total_seconds() / 60, 2) if remaining_time else 0,
                "hours": round(remaining_time.total_seconds() / 3600, 2) if remaining_time else 0
            },
            "expiration_warning": {
                "expires_soon": remaining_time.total_seconds() < 300 if remaining_time else True,  # 5 minutes
                "expires_very_soon": remaining_time.total_seconds() < 60 if remaining_time else True,  # 1 minute
                "should_refresh": remaining_time.total_seconds() < 600 if remaining_time else True  # 10 minutes
            }
        }
        
        return create_success_response(
            message="Expiration status retrieved successfully",
            data=expiration_status
        )
        
    except Exception as e:
        return create_error_response(
            message="Failed to get expiration status",
            errors=[str(e)],
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
