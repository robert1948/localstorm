from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean
from sqlalchemy.sql import func
from app.database import Base  # Updated import for new structure

class User(Base):
    """
    SQLAlchemy model for the users table.
    Stores user credentials, profile information, and role-based details.
    """
    __tablename__ = "users"

    # Basic fields
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True)
    hashed_password = Column(String(255))
    
    # Profile information
    first_name = Column(String(100))
    last_name = Column(String(100))
    phone = Column(String(20))
    website = Column(String(255))
    company = Column(String(255))
    
    # Role and experience
    role = Column(String(20))  # 'user' or 'developer'
    experience = Column(String(20))  # 'beginner', 'intermediate', 'advanced', 'expert'
    
    # Status and timestamps
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Terms acceptance
    terms_accepted_at = Column(DateTime(timezone=True))

class UserProfile(Base):
    """
    Extended profile information for users based on their role.
    """
    __tablename__ = "user_profiles"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)  # Foreign key to users.id
    
    # Role-specific data (stored as JSON-like text)
    profile_data = Column(Text)  # JSON string with role-specific fields
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())