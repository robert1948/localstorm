from pydantic import BaseModel, EmailStr, validator
from typing import Optional
from datetime import datetime
import re

# ----------------------------
# Schema: Enhanced User Registration (V2)
# ----------------------------
class UserCreateV2(BaseModel):
    """
    Schema for creating a new user with enhanced validation (2-step flow).
    """
    # Basic information
    email: EmailStr
    password: str
    firstName: str
    lastName: str
    
    # Role and company information
    role: str  # 'customer' or 'developer'
    company: Optional[str] = None
    phone: Optional[str] = None
    website: Optional[str] = None
    experience: Optional[str] = None
    
    @validator('password')
    def validate_password(cls, v):
        """Enhanced password validation for V2 registration"""
        if len(v) < 12:
            raise ValueError('Password must be at least 12 characters long')
        
        if not re.search(r'[A-Z]', v):
            raise ValueError('Password must contain at least one uppercase letter')
            
        if not re.search(r'[a-z]', v):
            raise ValueError('Password must contain at least one lowercase letter')
            
        if not re.search(r'[0-9]', v):
            raise ValueError('Password must contain at least one number')
            
        if not re.search(r'[^A-Za-z0-9]', v):
            raise ValueError('Password must contain at least one special character')
            
        return v
    
    @validator('firstName', 'lastName')
    def validate_names(cls, v):
        """Validate and sanitize names"""
        if not v or not v.strip():
            raise ValueError('Name cannot be empty')
        
        # Remove extra whitespace and limit length
        cleaned = v.strip()
        if len(cleaned) > 50:
            raise ValueError('Name must be 50 characters or less')
            
        return cleaned
    
    @validator('company')
    def validate_company(cls, v):
        """Validate and sanitize company name"""
        if v:
            cleaned = v.strip()
            if len(cleaned) > 100:
                raise ValueError('Company name must be 100 characters or less')
            return cleaned
        return v
    
    @validator('role')
    def validate_role(cls, v):
        """Validate role selection"""
        if v not in ['customer', 'developer']:
            raise ValueError('Role must be either "customer" or "developer"')
        return v
    
    @validator('website')
    def validate_website(cls, v):
        """Validate website URL format"""
        if v and v.strip():
            url = v.strip()
            if not re.match(r'^https?://', url):
                url = f'https://{url}'
            # Basic URL validation
            if not re.match(r'^https?://[^\s/$.?#].[^\s]*$', url):
                raise ValueError('Please enter a valid website URL')
            return url
        return v
    
    @validator('experience')
    def validate_experience(cls, v):
        """Validate experience level"""
        if v and v not in ['beginner', 'intermediate', 'advanced', 'expert']:
            raise ValueError('Experience must be one of: beginner, intermediate, advanced, expert')
        return v
    
    class Config:
        from_attributes = True

# ----------------------------
# Schema: User Registration (Original - for compatibility)
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
