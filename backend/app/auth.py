# backend/app/auth.py

from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
import bcrypt

# Try to use bcrypt directly if passlib has issues
try:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    USE_PASSLIB = True
except Exception as e:
    print(f"⚠️ Passlib bcrypt issue detected: {e}")
    USE_PASSLIB = False

def get_password_hash(password: str) -> str:
    """Hash password with fallback for bcrypt version issues"""
    if USE_PASSLIB:
        try:
            return pwd_context.hash(password)
        except Exception as e:
            print(f"⚠️ Passlib hash failed, using bcrypt directly: {e}")
    
    # Fallback to direct bcrypt usage
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password with fallback for bcrypt version issues"""
    if USE_PASSLIB:
        try:
            return pwd_context.verify(plain_password, hashed_password)
        except Exception as e:
            print(f"⚠️ Passlib verify failed, using bcrypt directly: {e}")
    
    # Fallback to direct bcrypt usage
    try:
        return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))
    except Exception:
        # If that fails, try the original passlib method as last resort
        return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, secret_key: str, algorithm: str, expires_delta: timedelta = timedelta(minutes=30)):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, secret_key, algorithm=algorithm)
