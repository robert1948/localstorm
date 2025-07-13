from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean
from sqlalchemy.sql import func
from app.database import Base  # Updated import for new structure

class User(Base):
    """
    SQLAlchemy model for the users table.
    Updated for production schema compatibility - July 13, 2025
    """
    __tablename__ = "users"

    # Basic fields - mapped to production schema
    id = Column(String, primary_key=True, index=True)  # UUID in production
    email = Column(String(255), unique=True, index=True)
    password_hash = Column(String(60))  # Match production column name
    
    # Profile information - mapped to production schema
    full_name = Column(String(100))  # Match production column name
    phone = Column(String(20))
    website = Column(String(255))
    company_name = Column(String)  # Match production column name
    
    # Role and experience - mapped to production schema
    user_role = Column(String(20))  # Match production column name
    experience = Column(String(20))  # 'beginner', 'intermediate', 'advanced', 'expert'
    
    # Production-specific fields
    industry = Column(String)
    project_budget = Column(String)
    skills = Column(String)
    portfolio = Column(String)
    github = Column(String)
    
    # Status and timestamps - match production schema
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Terms acceptance - use production column name
    tos_accepted_at = Column(DateTime(timezone=True))
    
    # Additional fields that might not exist in production yet
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)

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