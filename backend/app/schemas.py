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
    Updated for production database compatibility - July 13, 2025
    """
    id: str  # UUID string in production database
    email: EmailStr
    full_name: Optional[str] = None
    user_role: Optional[str] = None
    company_name: Optional[str] = None
    access_token: Optional[str] = None
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# ----------------------------
# Schema: Production Database Compatible Registration
# ----------------------------
class UserCreateV2Production(BaseModel):
    """
    Schema for creating a new user that matches production database schema.
    Updated for production compatibility - July 13, 2025
    """
    # Basic information - matches production columns
    email: EmailStr
    password: str
    full_name: str  # Single field instead of firstName/lastName
    
    # Role and company information - matches production columns
    user_role: str  # 'client' or 'developer' 
    company_name: Optional[str] = None
    
    # Production database additional fields
    industry: Optional[str] = None
    project_budget: Optional[str] = None
    skills: Optional[str] = None
    portfolio: Optional[str] = None
    github: Optional[str] = None
    
    # Terms acceptance
    tos_accepted: bool
    
    @validator('password')
    def validate_password(cls, v):
        """Enhanced password validation for V2 registration"""
        if len(v) < 8:  # Reduced from 12 for production compatibility
            raise ValueError('Password must be at least 8 characters long')
        
        if not re.search(r'[A-Z]', v):
            raise ValueError('Password must contain at least one uppercase letter')
            
        if not re.search(r'[a-z]', v):
            raise ValueError('Password must contain at least one lowercase letter')
            
        if not re.search(r'[0-9]', v):
            raise ValueError('Password must contain at least one number')
            
        return v
    
    @validator('full_name')
    def validate_full_name(cls, v):
        """Validate and sanitize full name"""
        if not v or not v.strip():
            raise ValueError('Full name cannot be empty')
        
        # Remove extra whitespace and limit length
        cleaned = v.strip()
        if len(cleaned) > 100:  # Match database column length
            raise ValueError('Full name must be 100 characters or less')
            
        return cleaned
    
    @validator('company_name')
    def validate_company_name(cls, v):
        """Validate and sanitize company name"""
        if v:
            cleaned = v.strip()
            if len(cleaned) > 255:  # Reasonable limit
                raise ValueError('Company name must be 255 characters or less')
            return cleaned
        return v
    
    @validator('user_role')
    def validate_user_role(cls, v):
        """Validate role selection"""
        if v not in ['client', 'developer']:
            raise ValueError('Role must be either "client" or "developer"')
        return v
    
    @validator('tos_accepted')
    def validate_tos_accepted(cls, v):
        """Ensure terms of service are accepted"""
        if not v:
            raise ValueError('Terms of service must be accepted')
        return v
    
    class Config:
        from_attributes = True

# ----------------------------
# Schema: 2-Step Registration Requests
# ----------------------------
class RegisterStep1Request(BaseModel):
    """Step 1: Email validation request"""
    email: EmailStr

class RegisterStep2Request(BaseModel):
    """Step 2: Complete registration request"""
    email: EmailStr
    password: str
    full_name: str
    user_role: Optional[str] = "client"  # Fixed: match database constraint
    company_name: Optional[str] = None
    
    @validator('password')
    def validate_password(cls, v):
        """Password validation for step 2"""
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        return v
    
    @validator('user_role')
    def validate_user_role(cls, v):
        """Validate role selection to match database constraint"""
        if v not in ['client', 'developer']:
            raise ValueError('Role must be either "client" or "developer"')
        return v
