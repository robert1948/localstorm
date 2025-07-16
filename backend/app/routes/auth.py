from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import os
from app.email_service import email_service

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
# Register Route (Enhanced)
# ----------------------------
@router.post("/auth/register", response_model=schemas.UserOut, tags=["auth"])
async def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(models.User).filter(models.User.email == user.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    hashed = get_password_hash(user.password)
    
    # Create user with enhanced fields
    db_user = models.User(
        email=user.email, 
        hashed_password=hashed,
        first_name=getattr(user, 'firstName', ''),
        last_name=getattr(user, 'lastName', ''),
        role=getattr(user, 'role', 'user'),
        company=getattr(user, 'company', ''),
        phone=getattr(user, 'phone', ''),
        website=getattr(user, 'website', ''),
        experience=getattr(user, 'experience', '')
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    # Send registration notification email
    try:
        user_data = {
            'firstName': getattr(user, 'firstName', ''),
            'lastName': getattr(user, 'lastName', ''),
            'email': user.email,
            'role': getattr(user, 'role', 'user'),
            'company': getattr(user, 'company', ''),
            'phone': getattr(user, 'phone', ''),
            'website': getattr(user, 'website', ''),
            'experience': getattr(user, 'experience', '')
        }
        
        await email_service.send_registration_notification(user_data)
        print(f"✅ Registration notification sent for {user.email}")
        
    except Exception as e:
        # Don't fail registration if email fails
        print(f"⚠️  Failed to send registration notification: {e}")
    
    return db_user

# ----------------------------
# JSON Login Route
# ----------------------------
@router.post("/auth/login", tags=["auth"])
def login(payload: schemas.LoginInput, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == payload.email).first()
    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    token = create_access_token({"sub": user.email}, SECRET_KEY, ALGORITHM)
    return {"access_token": token, "token_type": "bearer"}

# ----------------------------
# Email Validation Route (V2)
# ----------------------------
@router.get("/auth/validate-email/{email}", tags=["auth"])
async def validate_email(email: str, db: Session = Depends(get_db)):
    """
    Check if email is available for registration
    """
    try:
        # Validate email format
        from pydantic import EmailStr, ValidationError
        try:
            EmailStr.validate(email)
        except ValidationError:
            return {"available": False, "reason": "invalid_format"}
        
        # Check if email exists
        existing_user = db.query(models.User).filter(models.User.email == email.lower()).first()
        if existing_user:
            return {"available": False, "reason": "already_exists"}
        
        return {"available": True}
        
    except Exception as e:
        print(f"Email validation error: {e}")
        return {"available": None, "reason": "validation_error"}

# ----------------------------
# Enhanced Registration Route (V2)
# ----------------------------
@router.post("/auth/register/v2", response_model=schemas.UserOut, tags=["auth"])
async def register_v2(user: schemas.UserCreateV2, db: Session = Depends(get_db)):
    """
    Enhanced registration with stronger validation (V2 flow)
    """
    # Check for existing user
    existing_user = db.query(models.User).filter(models.User.email == user.email.lower()).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered. Please use a different email or try logging in."
        )
    
    # Hash password with enhanced security
    hashed = get_password_hash(user.password)
    
    # Create user with enhanced validation
    db_user = models.User(
        email=user.email.lower().strip(),
        hashed_password=hashed,
        first_name=user.firstName.strip(),
        last_name=user.lastName.strip(),
        role=user.role,
        company=user.company.strip() if user.company else None,
        phone=user.phone.strip() if user.phone else None,
        website=user.website if user.website else None,
        experience=user.experience if user.experience else None
    )
    
    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        
        # Send registration notification email (async)
        try:
            user_data = {
                'firstName': user.firstName,
                'lastName': user.lastName,
                'email': user.email,
                'role': user.role,
                'company': user.company or '',
                'phone': user.phone or '',
                'website': user.website or '',
                'experience': user.experience or ''
            }
            
            await email_service.send_registration_notification(user_data)
            print(f"✅ Registration notification sent for {user.email}")
            
        except Exception as e:
            # Don't fail registration if email fails
            print(f"⚠️  Failed to send registration notification: {e}")
        
        return db_user
        
    except Exception as e:
        db.rollback()
        print(f"Registration error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Registration failed. Please try again."
        )
