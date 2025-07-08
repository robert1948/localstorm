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
