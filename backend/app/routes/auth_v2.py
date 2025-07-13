from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
import os
import re
from typing import Optional

from app import models, schemas
from app.dependencies import get_db
from app.auth import get_password_hash, verify_password, create_access_token

router = APIRouter()

# Load secret key and algorithm from environment
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"

if not SECRET_KEY:
    raise RuntimeError("SECRET_KEY environment variable is not set.")

# ----------------------------
# Email Validation Endpoint
# ----------------------------
@router.get("/auth/v2/validate-email", tags=["auth-v2"])
async def validate_email(email: str, db: Session = Depends(get_db)):
    """
    Check if email is available for registration
    Returns: {"available": bool, "reason": str}
    """
    try:
        # Basic email format validation
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email):
            return {
                "available": False, 
                "reason": "invalid_format",
                "message": "Please enter a valid email address"
            }
        
        # Normalize email
        normalized_email = email.lower().strip()
        
        # Check if email exists in database
        existing_user = db.query(models.User).filter(
            models.User.email == normalized_email
        ).first()
        
        if existing_user:
            return {
                "available": False, 
                "reason": "already_exists",
                "message": "This email is already registered. Try logging in or use a different email."
            }
        
        return {
            "available": True,
            "message": "Email is available"
        }
        
    except Exception as e:
        print(f"❌ Email validation error: {e}")
        return {
            "available": None, 
            "reason": "validation_error",
            "message": "Unable to validate email. Please try again."
        }

# ----------------------------
# Password Strength Validation
# ----------------------------
@router.post("/auth/v2/validate-password", tags=["auth-v2"])
async def validate_password(password_data: dict):
    """
    Validate password strength
    Returns: {"valid": bool, "score": int, "requirements": dict}
    """
    password = password_data.get("password", "")
    
    requirements = {
        "minLength": len(password) >= 12,
        "hasUpper": bool(re.search(r'[A-Z]', password)),
        "hasLower": bool(re.search(r'[a-z]', password)),
        "hasNumber": bool(re.search(r'[0-9]', password)),
        "hasSpecial": bool(re.search(r'[^A-Za-z0-9]', password))
    }
    
    # Calculate strength score
    score = 0
    if requirements["minLength"]: score += 25
    if requirements["hasUpper"]: score += 20
    if requirements["hasLower"]: score += 20
    if requirements["hasNumber"]: score += 20
    if requirements["hasSpecial"]: score += 15
    
    all_valid = all(requirements.values())
    
    return {
        "valid": all_valid,
        "score": min(score, 100),
        "requirements": requirements,
        "message": "Strong password" if all_valid else "Password doesn't meet requirements"
    }

# ----------------------------
# Enhanced Registration Route (V2)
# ----------------------------
@router.post("/auth/v2/register", response_model=schemas.UserOut, tags=["auth-v2"])
async def register_v2(
    user: schemas.UserCreateV2, 
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """
    Enhanced registration with stronger validation and real-time feedback
    """
    try:
        # Normalize email
        normalized_email = user.email.lower().strip()
        
        # Double-check email availability
        existing_user = db.query(models.User).filter(
            models.User.email == normalized_email
        ).first()
        
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already registered. Please use a different email or try logging in."
            )
        
        # Hash password with enhanced security
        hashed_password = get_password_hash(user.password)
        
        # Create user record
        db_user = models.User(
            email=normalized_email,
            hashed_password=hashed_password,
            first_name=user.firstName.strip(),
            last_name=user.lastName.strip(),
            role=user.role,
            company=user.company.strip() if user.company else None,
            phone=user.phone.strip() if user.phone else None,
            website=user.website if user.website else None,
            experience=user.experience if user.experience else None,
            is_active=True,
            is_verified=False  # Will be verified via email
        )
        
        # Save to database
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        
        # Add background task for email notification
        background_tasks.add_task(
            send_welcome_email_task,
            {
                'firstName': user.firstName,
                'lastName': user.lastName,
                'email': user.email,
                'role': user.role,
                'company': user.company or '',
                'phone': user.phone or '',
                'website': user.website or '',
                'experience': user.experience or '',
                'userId': db_user.id
            }
        )
        
        print(f"✅ User registered successfully: {user.email} as {user.role}")
        
        return db_user
        
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except IntegrityError as e:
        db.rollback()
        print(f"❌ Database integrity error: {e}")
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered. Please use a different email."
        )
    except Exception as e:
        db.rollback()
        print(f"❌ Registration error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Registration failed. Please try again later."
        )

# ----------------------------
# Background Email Task
# ----------------------------
async def send_welcome_email_task(user_data: dict):
    """
    Send welcome email as background task
    """
    try:
        # Import here to avoid circular imports
        from app.email_service import email_service
        
        await email_service.send_registration_notification(user_data)
        print(f"✅ Welcome email sent to {user_data['email']}")
        
    except Exception as e:
        print(f"⚠️  Failed to send welcome email to {user_data['email']}: {e}")
        # Could implement retry logic here or add to failed email queue

# ----------------------------
# Enhanced Login Route (V2)
# ----------------------------
@router.post("/auth/v2/login", tags=["auth-v2"])
async def login_v2(payload: schemas.LoginInput, db: Session = Depends(get_db)):
    """
    Enhanced login with better error handling
    """
    try:
        # Normalize email
        normalized_email = payload.email.lower().strip()
        
        # Find user
        user = db.query(models.User).filter(
            models.User.email == normalized_email
        ).first()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )
        
        # Verify password
        if not verify_password(payload.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )
        
        # Check if account is active
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Account is deactivated. Please contact support."
            )
        
        # Create access token
        token_data = {
            "sub": user.email,
            "user_id": user.id,
            "role": user.role
        }
        access_token = create_access_token(token_data, SECRET_KEY, ALGORITHM)
        
        print(f"✅ User logged in: {user.email}")
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": {
                "id": user.id,
                "email": user.email,
                "firstName": user.first_name,
                "lastName": user.last_name,
                "role": user.role
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Login error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Login failed. Please try again."
        )
