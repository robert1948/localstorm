"""
Authentication Service for CapeAI Enterprise Platform
"""

import logging
import bcrypt
import jwt
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, Tuple
from sqlalchemy.orm import Session
from ..models import User
from ..database import get_db
from ..config import settings

logger = logging.getLogger(__name__)

class AuthService:
    """
    Enterprise authentication service with JWT token management,
    password hashing, and user session handling.
    """
    
    def __init__(self):
        self.secret_key = getattr(settings, 'SECRET_KEY', 'your-secret-key-here')
        self.algorithm = getattr(settings, 'JWT_ALGORITHM', 'HS256')
        self.access_token_expire_minutes = getattr(settings, 'ACCESS_TOKEN_EXPIRE_MINUTES', 1440)
        self.refresh_token_expire_days = getattr(settings, 'REFRESH_TOKEN_EXPIRE_DAYS', 30)
        logger.info("AuthService initialized")
    
    def hash_password(self, password: str) -> str:
        """
        Hash a password using bcrypt.
        
        Args:
            password: Plain text password
            
        Returns:
            Hashed password string
        """
        try:
            # Generate salt and hash password
            salt = bcrypt.gensalt(rounds=12)
            hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
            return hashed.decode('utf-8')
        except Exception as e:
            logger.error(f"Error hashing password: {e}")
            raise ValueError("Failed to hash password")
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """
        Verify a password against its hash.
        
        Args:
            plain_password: Plain text password
            hashed_password: Stored hashed password
            
        Returns:
            True if password matches, False otherwise
        """
        try:
            return bcrypt.checkpw(
                plain_password.encode('utf-8'), 
                hashed_password.encode('utf-8')
            )
        except Exception as e:
            logger.error(f"Error verifying password: {e}")
            return False
    
    def create_access_token(self, data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
        """
        Create a JWT access token.
        
        Args:
            data: Token payload data
            expires_delta: Custom expiration time
            
        Returns:
            JWT token string
        """
        try:
            to_encode = data.copy()
            
            if expires_delta:
                expire = datetime.utcnow() + expires_delta
            else:
                expire = datetime.utcnow() + timedelta(minutes=self.access_token_expire_minutes)
            
            to_encode.update({
                "exp": expire,
                "iat": datetime.utcnow(),
                "type": "access"
            })
            
            encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
            return encoded_jwt
        except Exception as e:
            logger.error(f"Error creating access token: {e}")
            raise ValueError("Failed to create access token")
    
    def create_refresh_token(self, data: Dict[str, Any]) -> str:
        """
        Create a JWT refresh token.
        
        Args:
            data: Token payload data
            
        Returns:
            JWT refresh token string
        """
        try:
            to_encode = data.copy()
            expire = datetime.utcnow() + timedelta(days=self.refresh_token_expire_days)
            
            to_encode.update({
                "exp": expire,
                "iat": datetime.utcnow(),
                "type": "refresh"
            })
            
            encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
            return encoded_jwt
        except Exception as e:
            logger.error(f"Error creating refresh token: {e}")
            raise ValueError("Failed to create refresh token")
    
    def verify_token(self, token: str) -> Optional[Dict[str, Any]]:
        """
        Verify and decode a JWT token.
        
        Args:
            token: JWT token string
            
        Returns:
            Decoded token payload or None if invalid
        """
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except jwt.ExpiredSignatureError:
            logger.warning("Token has expired")
            return None
        except jwt.InvalidTokenError as e:
            logger.warning(f"Invalid token: {e}")
            return None
        except Exception as e:
            logger.error(f"Error verifying token: {e}")
            return None
    
    def authenticate_user(self, db: Session, email: str, password: str) -> Optional[User]:
        """
        Authenticate a user with email and password.
        
        Args:
            db: Database session
            email: User email
            password: Plain text password
            
        Returns:
            User object if authenticated, None otherwise
        """
        try:
            # Find user by email
            user = db.query(User).filter(User.email == email).first()
            
            if not user:
                logger.warning(f"User not found: {email}")
                return None
            
            # Verify password
            if not self.verify_password(password, user.password_hash):
                logger.warning(f"Invalid password for user: {email}")
                return None
            
            logger.info(f"User authenticated successfully: {email}")
            return user
            
        except Exception as e:
            logger.error(f"Error authenticating user {email}: {e}")
            return None
    
    def create_user_tokens(self, user: User) -> Dict[str, str]:
        """
        Create access and refresh tokens for user.
        
        Args:
            user: User object
            
        Returns:
            Dictionary with access_token and refresh_token
        """
        try:
            # Token payload
            token_data = {
                "user_id": user.id,
                "email": user.email,
                "user_role": getattr(user, 'user_role', 'user')
            }
            
            # Create tokens
            access_token = self.create_access_token(token_data)
            refresh_token = self.create_refresh_token({"user_id": user.id})
            
            return {
                "access_token": access_token,
                "refresh_token": refresh_token,
                "token_type": "bearer"
            }
        except Exception as e:
            logger.error(f"Error creating user tokens: {e}")
            raise ValueError("Failed to create user tokens")
    
    def refresh_access_token(self, refresh_token: str, db: Session) -> Optional[Dict[str, str]]:
        """
        Create new access token from refresh token.
        
        Args:
            refresh_token: JWT refresh token
            db: Database session
            
        Returns:
            New token dictionary or None if invalid
        """
        try:
            # Verify refresh token
            payload = self.verify_token(refresh_token)
            
            if not payload or payload.get("type") != "refresh":
                logger.warning("Invalid refresh token")
                return None
            
            # Get user
            user_id = payload.get("user_id")
            user = db.query(User).filter(User.id == user_id).first()
            
            if not user:
                logger.warning(f"User not found for refresh token: {user_id}")
                return None
            
            # Create new access token
            token_data = {
                "user_id": user.id,
                "email": user.email,
                "user_role": getattr(user, 'user_role', 'user')
            }
            
            access_token = self.create_access_token(token_data)
            
            return {
                "access_token": access_token,
                "token_type": "bearer"
            }
            
        except Exception as e:
            logger.error(f"Error refreshing access token: {e}")
            return None
    
    def get_current_user(self, token: str, db: Session) -> Optional[User]:
        """
        Get current user from JWT token.
        
        Args:
            token: JWT access token
            db: Database session
            
        Returns:
            User object or None if invalid
        """
        try:
            # Verify token
            payload = self.verify_token(token)
            
            if not payload or payload.get("type") != "access":
                return None
            
            # Get user
            user_id = payload.get("user_id")
            user = db.query(User).filter(User.id == user_id).first()
            
            return user
            
        except Exception as e:
            logger.error(f"Error getting current user: {e}")
            return None
    
    def validate_password_strength(self, password: str) -> Tuple[bool, str]:
        """
        Validate password strength.
        
        Args:
            password: Plain text password
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        try:
            errors = []
            
            if len(password) < 8:
                errors.append("Password must be at least 8 characters long")
            
            if not any(c.isupper() for c in password):
                errors.append("Password must contain at least one uppercase letter")
            
            if not any(c.islower() for c in password):
                errors.append("Password must contain at least one lowercase letter")
            
            if not any(c.isdigit() for c in password):
                errors.append("Password must contain at least one number")
            
            if not any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password):
                errors.append("Password must contain at least one special character")
            
            if errors:
                return False, "; ".join(errors)
            
            return True, "Password is strong"
            
        except Exception as e:
            logger.error(f"Error validating password: {e}")
            return False, "Error validating password"

# Global auth service instance
auth_service = AuthService()

def get_auth_service() -> AuthService:
    """Get the global auth service instance."""
    return auth_service