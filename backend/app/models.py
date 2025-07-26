from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.database import Base  # Updated import for new structure

class User(Base):
    """
    SQLAlchemy model for the users table.
    Updated for production schema compatibility - July 13, 2025
    Only includes columns that exist in production database
    """
    __tablename__ = "users"
    __table_args__ = {"extend_existing": True}
    
    # Production database columns only
    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))  # UUID generator
    email = Column(String(255), unique=True, index=True)
    password_hash = Column(String(60))
    user_role = Column(String(20))
    full_name = Column(String(100))
    tos_accepted_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    company_name = Column(String)
    industry = Column(String)
    project_budget = Column(String)
    skills = Column(String)
    portfolio = Column(String)
    github = Column(String)

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