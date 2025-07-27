"""
User Service for CapeAI Enterprise Platform
"""

import logging
from typing import Optional, Dict, Any, List
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, desc
from datetime import datetime, timedelta
from ..models import User
from ..database import get_db
from ..config import settings
from .auth_service import get_auth_service

logger = logging.getLogger(__name__)

class UserService:
    """
    Enterprise user management service with profile management,
    preferences, and user analytics.
    """
    
    def __init__(self):
        self.auth_service = get_auth_service()
        logger.info("UserService initialized")
    
    async def create_user(self, db: Session, user_data: Dict[str, Any]) -> Optional[User]:
        """
        Create a new user account.
        
        Args:
            db: Database session
            user_data: User registration data
            
        Returns:
            Created User object or None if failed
        """
        try:
            # Validate required fields
            required_fields = ['email', 'password', 'full_name']
            for field in required_fields:
                if not user_data.get(field):
                    logger.error(f"Missing required field: {field}")
                    return None
            
            # Check if user already exists
            existing_user = db.query(User).filter(User.email == user_data['email']).first()
            if existing_user:
                logger.warning(f"User already exists: {user_data['email']}")
                return None
            
            # Hash password
            hashed_password = self.auth_service.hash_password(user_data['password'])
            
            # Create user object
            user = User(
                email=user_data['email'],
                password_hash=hashed_password,
                full_name=user_data['full_name'],
                user_role=user_data.get('user_role', 'user'),
                company_name=user_data.get('company_name'),
                industry=user_data.get('industry'),
                project_budget=user_data.get('project_budget'),
                skills=user_data.get('skills'),
                portfolio=user_data.get('portfolio'),
                github=user_data.get('github'),
                tos_accepted_at=datetime.utcnow()
            )
            
            # Save to database
            db.add(user)
            db.commit()
            db.refresh(user)
            
            logger.info(f"User created successfully: {user.email}")
            return user
            
        except Exception as e:
            logger.error(f"Error creating user: {e}")
            db.rollback()
            return None
    
    async def get_user_by_id(self, db: Session, user_id: str) -> Optional[User]:
        """
        Get user by ID.
        
        Args:
            db: Database session
            user_id: User ID
            
        Returns:
            User object or None if not found
        """
        try:
            user = db.query(User).filter(User.id == user_id).first()
            return user
        except Exception as e:
            logger.error(f"Error getting user by ID {user_id}: {e}")
            return None
    
    async def get_user_by_email(self, db: Session, email: str) -> Optional[User]:
        """
        Get user by email address.
        
        Args:
            db: Database session
            email: User email
            
        Returns:
            User object or None if not found
        """
        try:
            user = db.query(User).filter(User.email == email).first()
            return user
        except Exception as e:
            logger.error(f"Error getting user by email {email}: {e}")
            return None
    
    async def update_user(self, db: Session, user_id: str, updates: Dict[str, Any]) -> Optional[User]:
        """
        Update user information.
        
        Args:
            db: Database session
            user_id: User ID
            updates: Dictionary of fields to update
            
        Returns:
            Updated User object or None if failed
        """
        try:
            user = await self.get_user_by_id(db, user_id)
            if not user:
                logger.warning(f"User not found for update: {user_id}")
                return None
            
            # Update allowed fields
            allowed_fields = [
                'full_name', 'company_name', 'industry', 'project_budget',
                'skills', 'portfolio', 'github', 'user_role'
            ]
            
            for field, value in updates.items():
                if field in allowed_fields and hasattr(user, field):
                    setattr(user, field, value)
            
            # Update timestamp
            user.updated_at = datetime.utcnow()
            
            db.commit()
            db.refresh(user)
            
            logger.info(f"User updated successfully: {user_id}")
            return user
            
        except Exception as e:
            logger.error(f"Error updating user {user_id}: {e}")
            db.rollback()
            return None
    
    async def change_password(self, db: Session, user_id: str, current_password: str, new_password: str) -> bool:
        """
        Change user password.
        
        Args:
            db: Database session
            user_id: User ID
            current_password: Current password
            new_password: New password
            
        Returns:
            True if successful, False otherwise
        """
        try:
            user = await self.get_user_by_id(db, user_id)
            if not user:
                logger.warning(f"User not found for password change: {user_id}")
                return False
            
            # Verify current password
            if not self.auth_service.verify_password(current_password, user.password_hash):
                logger.warning(f"Invalid current password for user: {user_id}")
                return False
            
            # Validate new password strength
            is_valid, error_message = self.auth_service.validate_password_strength(new_password)
            if not is_valid:
                logger.warning(f"Weak password for user {user_id}: {error_message}")
                return False
            
            # Hash new password
            new_hash = self.auth_service.hash_password(new_password)
            user.password_hash = new_hash
            user.updated_at = datetime.utcnow()
            
            db.commit()
            logger.info(f"Password changed successfully for user: {user_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error changing password for user {user_id}: {e}")
            db.rollback()
            return False
    
    async def get_user_profile(self, db: Session, user_id: str) -> Optional[Dict[str, Any]]:
        """
        Get comprehensive user profile.
        
        Args:
            db: Database session
            user_id: User ID
            
        Returns:
            User profile dictionary or None if not found
        """
        try:
            user = await self.get_user_by_id(db, user_id)
            if not user:
                return None
            
            # Build comprehensive profile
            profile = {
                "id": user.id,
                "email": user.email,
                "full_name": user.full_name,
                "user_role": user.user_role,
                "company_name": user.company_name,
                "industry": user.industry,
                "project_budget": user.project_budget,
                "skills": user.skills,
                "portfolio": user.portfolio,
                "github": user.github,
                "created_at": user.created_at.isoformat() if user.created_at else None,
                "updated_at": user.updated_at.isoformat() if user.updated_at else None,
                "tos_accepted_at": user.tos_accepted_at.isoformat() if user.tos_accepted_at else None
            }
            
            return profile
            
        except Exception as e:
            logger.error(f"Error getting user profile {user_id}: {e}")
            return None
    
    async def search_users(self, db: Session, query: str, limit: int = 50) -> List[Dict[str, Any]]:
        """
        Search users by name, email, or company.
        
        Args:
            db: Database session
            query: Search query
            limit: Maximum results
            
        Returns:
            List of user dictionaries
        """
        try:
            search_term = f"%{query}%"
            
            users = db.query(User).filter(
                or_(
                    User.full_name.ilike(search_term),
                    User.email.ilike(search_term),
                    User.company_name.ilike(search_term)
                )
            ).limit(limit).all()
            
            results = []
            for user in users:
                results.append({
                    "id": user.id,
                    "email": user.email,
                    "full_name": user.full_name,
                    "company_name": user.company_name,
                    "user_role": user.user_role,
                    "created_at": user.created_at.isoformat() if user.created_at else None
                })
            
            return results
            
        except Exception as e:
            logger.error(f"Error searching users: {e}")
            return []
    
    async def get_user_statistics(self, db: Session, user_id: str) -> Dict[str, Any]:
        """
        Get user activity statistics.
        
        Args:
            db: Database session
            user_id: User ID
            
        Returns:
            Statistics dictionary
        """
        try:
            user = await self.get_user_by_id(db, user_id)
            if not user:
                return {}
            
            # Calculate user statistics
            stats = {
                # Account information
                "account_age_days": (datetime.utcnow() - user.created_at).days if user.created_at else 0,
                "last_update": user.updated_at.isoformat() if user.updated_at else None,
                "profile_completion": self._calculate_profile_completion(user),
                
                # Activity metrics (would be enhanced with actual usage data)
                "total_conversations": 0,  # Would connect to conversation tracking
                "total_messages": 0,       # Would connect to message tracking
                "ai_interactions": 0,      # Would connect to AI usage tracking
                
                # User classification
                "user_type": self._classify_user_type(user),
                "experience_level": self._determine_experience_level(user)
            }
            
            return stats
            
        except Exception as e:
            logger.error(f"Error getting user statistics {user_id}: {e}")
            return {}
    
    async def deactivate_user(self, db: Session, user_id: str, reason: str = None) -> bool:
        """
        Deactivate user account.
        
        Args:
            db: Database session
            user_id: User ID
            reason: Deactivation reason
            
        Returns:
            True if successful, False otherwise
        """
        try:
            user = await self.get_user_by_id(db, user_id)
            if not user:
                logger.warning(f"User not found for deactivation: {user_id}")
                return False
            
            # Mark as inactive (assuming is_active field exists)
            if hasattr(user, 'is_active'):
                user.is_active = False
            
            user.updated_at = datetime.utcnow()
            
            db.commit()
            logger.info(f"User deactivated: {user_id} - Reason: {reason}")
            return True
            
        except Exception as e:
            logger.error(f"Error deactivating user {user_id}: {e}")
            db.rollback()
            return False
    
    def _calculate_profile_completion(self, user: User) -> float:
        """Calculate profile completion percentage."""
        try:
            total_fields = 8
            completed_fields = 0
            
            # Check essential fields
            if user.email: completed_fields += 1
            if user.full_name: completed_fields += 1
            if user.company_name: completed_fields += 1
            if user.industry: completed_fields += 1
            if user.project_budget: completed_fields += 1
            if user.skills: completed_fields += 1
            if user.portfolio: completed_fields += 1
            if user.github: completed_fields += 1
            
            return round((completed_fields / total_fields) * 100, 1)
        except:
            return 0.0
    
    def _classify_user_type(self, user: User) -> str:
        """Classify user type based on profile."""
        try:
            if user.user_role == 'admin':
                return 'admin'
            elif user.company_name and user.industry:
                return 'business'
            elif user.github or user.portfolio:
                return 'developer'
            else:
                return 'individual'
        except:
            return 'unknown'
    
    def _determine_experience_level(self, user: User) -> str:
        """Determine user experience level."""
        try:
            # Simple heuristic based on profile completeness and fields
            completion = self._calculate_profile_completion(user)
            
            if completion >= 80 and (user.portfolio or user.github):
                return 'expert'
            elif completion >= 60:
                return 'intermediate'
            else:
                return 'beginner'
        except:
            return 'unknown'

# Global user service instance
user_service = UserService()

def get_user_service() -> UserService:
    """Get the global user service instance."""
    return user_service