from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
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

    # Relationships
    conversations = relationship("Conversation", back_populates="user")

class UserProfile(Base):
    """
    Extended profile information for users based on their role.
    """
    __tablename__ = "user_profiles"
    __table_args__ = {"extend_existing": True}
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)  # Foreign key to users.id
    
    # Role-specific data (stored as JSON-like text)
    profile_data = Column(Text)  # JSON string with role-specific fields
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class Conversation(Base):
    """
    SQLAlchemy model for conversations between users and AI.
    """
    __tablename__ = "conversations"
    __table_args__ = {"extend_existing": True}
    
    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"), index=True)
    title = Column(String(255))
    status = Column(String(20), default="active")  # active, archived, deleted
    
    # Conversation metadata
    total_messages = Column(Integer, default=0)
    ai_provider = Column(String(50))  # openai, anthropic, gemini
    model_name = Column(String(100))
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="conversations")
    messages = relationship("ConversationMessage", back_populates="conversation")

class ConversationMessage(Base):
    """
    SQLAlchemy model for individual messages within conversations.
    """
    __tablename__ = "conversation_messages"
    __table_args__ = {"extend_existing": True}
    
    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    conversation_id = Column(String, ForeignKey("conversations.id"), index=True)
    
    # Message content
    role = Column(String(20))  # user, assistant, system
    content = Column(Text)
    tokens_used = Column(Integer, default=0)
    
    # Message metadata
    ai_provider = Column(String(50))
    model_name = Column(String(100))
    response_time_ms = Column(Integer)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    conversation = relationship("Conversation", back_populates="messages")