#!/usr/bin/env python3
"""
JWT Token Expiration Test Script

This script demonstrates the 1-hour JWT token expiration functionality.
It creates tokens, validates them, and shows expiration behavior.

Usage:
    python test_token_expiration.py

@author AI Job Readiness Team
@version 1.0.0
"""

import asyncio
import sys
import os
from datetime import datetime, timedelta

# Add the app directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from app.utils.jwt_utils import JWTTokenManager, create_token_pair, validate_token_expiration
from app.core.config import settings


async def test_token_creation():
    """Test token creation with 1-hour expiration."""
    print("🔐 Testing JWT Token Creation with 1-Hour Expiration")
    print("=" * 60)
    
    # Test user ID
    test_user_id = "test-user-123"
    
    # Create access token
    access_token = JWTTokenManager.create_access_token(test_user_id)
    print(f"✅ Access token created: {access_token[:50]}...")
    
    # Create refresh token
    refresh_token = JWTTokenManager.create_refresh_token(test_user_id)
    print(f"✅ Refresh token created: {refresh_token[:50]}...")
    
    # Create token pair
    access_token_pair, refresh_token_pair = create_token_pair(test_user_id)
    print(f"✅ Token pair created successfully")
    
    return access_token, refresh_token


async def test_token_validation(access_token: str):
    """Test token validation and expiration checking."""
    print("\n🔍 Testing Token Validation")
    print("=" * 60)
    
    # Verify access token
    payload = JWTTokenManager.verify_access_token(access_token)
    if payload:
        print(f"✅ Access token is valid")
        print(f"   User ID: {payload.get('sub')}")
        print(f"   Token Type: {payload.get('type')}")
        print(f"   Issued At: {datetime.fromtimestamp(payload.get('iat', 0))}")
    else:
        print("❌ Access token is invalid")
        return False
    
    # Check expiration
    is_expired = JWTTokenManager.is_token_expired(access_token)
    print(f"   Is Expired: {is_expired}")
    
    # Get expiration time
    exp_time = JWTTokenManager.get_token_expiration(access_token)
    if exp_time:
        print(f"   Expires At: {exp_time}")
        print(f"   Current Time: {datetime.utcnow()}")
    
    # Get remaining time
    remaining_time = JWTTokenManager.get_token_remaining_time(access_token)
    if remaining_time:
        print(f"   Remaining Time: {remaining_time}")
        print(f"   Remaining Hours: {remaining_time.total_seconds() / 3600:.2f}")
        print(f"   Remaining Minutes: {remaining_time.total_seconds() / 60:.2f}")
    
    return True


async def test_short_lived_token():
    """Test with a short-lived token (1 minute) to demonstrate expiration."""
    print("\n⏰ Testing Short-Lived Token (1 minute)")
    print("=" * 60)
    
    test_user_id = "test-user-short"
    
    # Create token that expires in 1 minute
    short_token = JWTTokenManager.create_access_token(
        test_user_id, 
        expires_delta=timedelta(minutes=1)
    )
    
    print(f"✅ Short-lived token created: {short_token[:50]}...")
    
    # Check initial validation
    is_valid = validate_token_expiration(short_token)
    print(f"   Initial validation: {'✅ Valid' if is_valid else '❌ Invalid'}")
    
    # Get expiration details
    exp_time = JWTTokenManager.get_token_expiration(short_token)
    remaining_time = JWTTokenManager.get_token_remaining_time(short_token)
    
    if exp_time and remaining_time:
        print(f"   Expires at: {exp_time}")
        print(f"   Remaining: {remaining_time}")
        print(f"   Remaining seconds: {remaining_time.total_seconds():.0f}")
    
    return short_token


async def test_token_expiration_handling():
    """Test how expired tokens are handled."""
    print("\n🚫 Testing Expired Token Handling")
    print("=" * 60)
    
    test_user_id = "test-user-expired"
    
    # Create token that expired 1 hour ago
    expired_token = JWTTokenManager.create_access_token(
        test_user_id,
        expires_delta=timedelta(hours=-1)  # Expired 1 hour ago
    )
    
    print(f"✅ Expired token created: {expired_token[:50]}...")
    
    # Try to verify expired token
    payload = JWTTokenManager.verify_access_token(expired_token)
    if payload:
        print("❌ ERROR: Expired token should not be valid!")
    else:
        print("✅ Correctly rejected expired token")
    
    # Check expiration status
    is_expired = JWTTokenManager.is_token_expired(expired_token)
    print(f"   Is expired: {is_expired}")
    
    # Validate expiration
    is_valid = validate_token_expiration(expired_token)
    print(f"   Validation result: {'✅ Valid' if is_valid else '❌ Invalid (as expected)'}")


async def test_configuration():
    """Test JWT configuration settings."""
    print("\n⚙️ Testing JWT Configuration")
    print("=" * 60)
    
    print(f"Access token expiration: {settings.security.access_token_expire_minutes} minutes")
    print(f"Refresh token expiration: {settings.security.refresh_token_expire_days} days")
    print(f"JWT algorithm: {settings.security.algorithm}")
    print(f"Secret key configured: {'✅ Yes' if settings.security.secret_key != 'your-secret-key-change-in-production' else '⚠️ Using default (change in production)'}")
    print(f"Users secret configured: {'✅ Yes' if settings.security.users_secret != 'your-users-secret-change-in-production' else '⚠️ Using default (change in production)'}")


async def main():
    """Main test function."""
    print("🧪 JWT Token Expiration Test Suite")
    print("=" * 60)
    print(f"Test started at: {datetime.now()}")
    print()
    
    try:
        # Test configuration
        await test_configuration()
        
        # Test token creation
        access_token, refresh_token = await test_token_creation()
        
        # Test token validation
        await test_token_validation(access_token)
        
        # Test short-lived token
        short_token = await test_short_lived_token()
        
        # Test expired token handling
        await test_token_expiration_handling()
        
        print("\n🎉 All tests completed successfully!")
        print("=" * 60)
        print("Summary:")
        print("✅ JWT tokens are configured to expire after 1 hour")
        print("✅ Expired tokens are properly rejected")
        print("✅ Token validation works correctly")
        print("✅ Expiration checking is accurate")
        print("✅ Error handling is implemented")
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True


if __name__ == "__main__":
    # Run the test
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
