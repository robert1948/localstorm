from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

# ----------------------------
# Schema: User Registration (Enhanced)
# ----------------------------
class UserCreate(BaseModel):
    """
    Schema for creating a new user with enhanced registration data.
    """
    # Basic information
    email: EmailStr
    password: str
    firstName: str
    lastName: str
    
    # Role and company information
    role: str  # 'user' or 'developer'
    company: Optional[str] = None
    phone: Optional[str] = None
    website: Optional[str] = None
    experience: Optional[str] = None
    
    class Config:
        from_attributes = True

# ----------------------------
# Schema: Basic User Registration (Step 1)
# ----------------------------
class BasicUserCreate(BaseModel):
    """
    Schema for the first step of registration.
    """
    email: EmailStr
    password: str
    firstName: str
    lastName: str

# ----------------------------
# Schema: User Login (JSON input)
# ----------------------------
class LoginInput(BaseModel):
    """
    Schema for user login via JSON.
    """
    email: EmailStr
    password: str


# ----------------------------
# Schema: Public User Info (safe output)
# ----------------------------
class UserOut(BaseModel):
    """
    Schema for returning user information (excluding sensitive data).
    """
    id: int
    email: EmailStr

    class Config:
        from_attributes = True
