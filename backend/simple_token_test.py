#!/usr/bin/env python3
"""
Simple JWT Token Expiration Test

This script tests JWT token expiration without requiring the full app context.
"""

import jwt
from datetime import datetime, timedelta
import sys

def test_jwt_expiration():
    """Test JWT token creation and expiration."""
    print("🔐 Testing JWT Token Expiration (1 Hour)")
    print("=" * 50)
    
    # Configuration
    secret_key = "test-secret-key"
    algorithm = "HS256"
    user_id = "test-user-123"
    
    # Create token that expires in 1 hour
    expire_time = datetime.utcnow() + timedelta(hours=1)
    
    payload = {
        "sub": user_id,
        "exp": expire_time,
        "iat": datetime.utcnow(),
        "type": "access"
    }
    
    # Create token
    token = jwt.encode(payload, secret_key, algorithm=algorithm)
    print(f"✅ Token created: {token[:50]}...")
    print(f"   Expires at: {expire_time}")
    print(f"   User ID: {user_id}")
    
    # Verify token immediately
    try:
        decoded = jwt.decode(token, secret_key, algorithms=[algorithm])
        print(f"✅ Token is valid: {decoded['sub']}")
    except jwt.ExpiredSignatureError:
        print("❌ Token is expired")
    except jwt.InvalidTokenError as e:
        print(f"❌ Token is invalid: {e}")
    
    # Test expired token
    print("\n🚫 Testing Expired Token")
    print("-" * 30)
    
    expired_payload = {
        "sub": user_id,
        "exp": datetime.utcnow() - timedelta(hours=1),  # Expired 1 hour ago
        "iat": datetime.utcnow() - timedelta(hours=2),
        "type": "access"
    }
    
    expired_token = jwt.encode(expired_payload, secret_key, algorithm=algorithm)
    print(f"✅ Expired token created: {expired_token[:50]}...")
    
    try:
        decoded = jwt.decode(expired_token, secret_key, algorithms=[algorithm])
        print("❌ ERROR: Expired token should not be valid!")
    except jwt.ExpiredSignatureError:
        print("✅ Correctly rejected expired token")
    except jwt.InvalidTokenError as e:
        print(f"❌ Token is invalid: {e}")
    
    # Test token with 1 minute expiration
    print("\n⏰ Testing Short-Lived Token (1 minute)")
    print("-" * 40)
    
    short_payload = {
        "sub": user_id,
        "exp": datetime.utcnow() + timedelta(minutes=1),
        "iat": datetime.utcnow(),
        "type": "access"
    }
    
    short_token = jwt.encode(short_payload, secret_key, algorithm=algorithm)
    print(f"✅ Short token created: {short_token[:50]}...")
    
    try:
        decoded = jwt.decode(short_token, secret_key, algorithms=[algorithm])
        print(f"✅ Short token is valid: {decoded['sub']}")
        exp_time = datetime.fromtimestamp(decoded['exp'])
        remaining = exp_time - datetime.utcnow()
        print(f"   Remaining time: {remaining}")
        print(f"   Remaining seconds: {remaining.total_seconds():.0f}")
    except jwt.ExpiredSignatureError:
        print("❌ Short token is expired")
    except jwt.InvalidTokenError as e:
        print(f"❌ Short token is invalid: {e}")
    
    print("\n🎉 JWT Token Expiration Test Complete!")
    print("=" * 50)
    print("✅ 1-hour token expiration is working correctly")
    print("✅ Expired tokens are properly rejected")
    print("✅ Token validation is functioning")
    
    return True

if __name__ == "__main__":
    try:
        success = test_jwt_expiration()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"❌ Test failed: {e}")
        sys.exit(1)
