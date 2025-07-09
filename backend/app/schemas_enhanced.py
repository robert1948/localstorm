"""
Enhanced Pydantic Schemas for Secure Authentication
=================================================

This file implements schemas for the proposed secure authentication architecture:
- Role-based user creation and responses
- JWT token management
- Developer earnings tracking
- Password reset workflows
- Audit logging
"""

from pydantic import BaseModel, EmailStr, validator
from typing import Optional, List
from datetime import datetime
from decimal import Decimal
from enum import Enum

# Role enum for validation
class UserRole(str, Enum):
    CUSTOMER = "customer"
    DEVELOPER = "developer"
    ADMIN = "admin"

class TokenType(str, Enum):
    ACCESS = "access"
    REFRESH = "refresh"
    RESET = "reset"

# ================================
# User Schemas
# ================================

class UserCreate(BaseModel):
    """Schema for user registration"""
    email: EmailStr
    password: str
    first_name: str
    last_name: str
    role: UserRole
    company: Optional[str] = None
    phone: Optional[str] = None
    website: Optional[str] = None
    experience: Optional[str] = None
    
    @validator('password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        return v
    
    @validator('role')
    def validate_role(cls, v):
        if v not in [UserRole.CUSTOMER, UserRole.DEVELOPER]:
            raise ValueError('Role must be customer or developer for registration')
        return v

class UserLogin(BaseModel):
    """Schema for user login"""
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    """Schema for user data response (excludes sensitive data)"""
    id: int
    email: str
    role: UserRole
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    company: Optional[str] = None
    phone: Optional[str] = None
    website: Optional[str] = None
    experience: Optional[str] = None
    is_active: bool
    is_verified: bool
    created_at: datetime
    last_login_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    """Schema for updating user profile"""
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    company: Optional[str] = None
    phone: Optional[str] = None
    website: Optional[str] = None
    experience: Optional[str] = None

class PasswordChange(BaseModel):
    """Schema for password change"""
    current_password: str
    new_password: str
    
    @validator('new_password')
    def validate_new_password(cls, v):
        if len(v) < 8:
            raise ValueError('New password must be at least 8 characters long')
        return v

# ================================
# Authentication Schemas
# ================================

class TokenResponse(BaseModel):
    """Schema for token response"""
    access_token: str
    refresh_token: Optional[str] = None
    token_type: str = "bearer"
    expires_in: int  # seconds
    user: UserResponse

class TokenRefresh(BaseModel):
    """Schema for token refresh"""
    refresh_token: str

class TokenRevoke(BaseModel):
    """Schema for token revocation"""
    token: str
    token_type: TokenType = TokenType.ACCESS

# ================================
# Password Reset Schemas
# ================================

class PasswordResetRequest(BaseModel):
    """Schema for password reset request"""
    email: EmailStr

class PasswordResetConfirm(BaseModel):
    """Schema for password reset confirmation"""
    token: str
    new_password: str
    
    @validator('new_password')
    def validate_new_password(cls, v):
        if len(v) < 8:
            raise ValueError('New password must be at least 8 characters long')
        return v

class PasswordResetResponse(BaseModel):
    """Schema for password reset response"""
    message: str
    email_sent: bool

# ================================
# Developer Earnings Schemas
# ================================

class DeveloperEarningResponse(BaseModel):
    """Schema for developer earnings response"""
    id: int
    agent_id: str
    agent_name: Optional[str] = None
    revenue_share: Decimal
    total_sales: Decimal
    commission_rate: Decimal
    last_payout_amount: Decimal
    last_payout_at: Optional[datetime] = None
    total_paid_out: Decimal
    currency: str
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class DeveloperEarningsCreate(BaseModel):
    """Schema for creating developer earnings record"""
    agent_id: str
    agent_name: str
    commission_rate: Optional[Decimal] = Decimal('0.3000')
    currency: Optional[str] = "USD"

class DeveloperEarningsUpdate(BaseModel):
    """Schema for updating developer earnings"""
    agent_name: Optional[str] = None
    commission_rate: Optional[Decimal] = None
    is_active: Optional[bool] = None

class DeveloperEarningsSummary(BaseModel):
    """Schema for developer earnings summary"""
    total_agents: int
    total_revenue_share: Decimal
    total_sales: Decimal
    total_paid_out: Decimal
    pending_payout: Decimal
    currency: str
    earnings: List[DeveloperEarningResponse]

# ================================
# Audit Log Schemas
# ================================

class AuditLogResponse(BaseModel):
    """Schema for audit log response"""
    id: int
    user_id: Optional[int] = None
    event_type: str
    event_description: Optional[str] = None
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    endpoint: Optional[str] = None
    success: bool
    error_message: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True

# ================================
# API Response Schemas
# ================================

class ApiResponse(BaseModel):
    """Generic API response schema"""
    success: bool
    message: str
    data: Optional[dict] = None

class ErrorResponse(BaseModel):
    """Error response schema"""
    success: bool = False
    error: str
    detail: Optional[str] = None
    code: Optional[str] = None

# ================================
# Validation Schemas
# ================================

class EmailValidation(BaseModel):
    """Schema for email validation"""
    email: EmailStr

class TokenValidation(BaseModel):
    """Schema for token validation"""
    token: str
    token_type: Optional[TokenType] = TokenType.ACCESS

# ================================
# Admin Schemas
# ================================

class UserAdminResponse(UserResponse):
    """Extended user response for admin endpoints"""
    email_verified_at: Optional[datetime] = None
    terms_accepted_at: Optional[datetime] = None
    privacy_accepted_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class UserAdminUpdate(BaseModel):
    """Schema for admin user updates"""
    is_active: Optional[bool] = None
    is_verified: Optional[bool] = None
    role: Optional[UserRole] = None
    
class BulkUserOperation(BaseModel):
    """Schema for bulk user operations"""
    user_ids: List[int]
    operation: str  # 'activate', 'deactivate', 'verify', 'delete'
