from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
import os
import re
from typing import Optional
from datetime import datetime

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
    user: schemas.UserCreateV2Production, 
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
        
        # Create user record with production schema
        db_user = models.User(
            email=normalized_email,
            password_hash=hashed_password,  # Production column name
            full_name=user.full_name.strip(),  # Production field
            user_role=user.user_role,  # Production column name
            company_name=user.company_name.strip() if user.company_name else None,  # Production column name
            industry=user.industry.strip() if user.industry else None,
            project_budget=user.project_budget.strip() if user.project_budget else None,
            skills=user.skills.strip() if user.skills else None,
            portfolio=user.portfolio.strip() if user.portfolio else None,
            github=user.github.strip() if user.github else None,
            tos_accepted_at=datetime.utcnow()  # Production column name
        )
        
        # Save to database
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        
        # Add background task for email notification
        background_tasks.add_task(
            send_welcome_email_task,
            {
                'full_name': user.full_name,
                'email': user.email,
                'user_role': user.user_role,
                'company_name': user.company_name or '',
                'industry': user.industry or '',
                'project_budget': user.project_budget or '',
                'skills': user.skills or '',
                'portfolio': user.portfolio or '',
                'github': user.github or '',
                'userId': db_user.id
            }
        )
        
        print(f"✅ User registered successfully: {user.email} as {user.user_role}")
        
        # Return user with explicit string conversion for UUID
        return {"id": str(db_user.id), "email": db_user.email}
        
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
        
        # Verify password using production column name
        if not verify_password(payload.password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )
        
        # Check if account is active (skip this check for production compatibility)
        # if not user.is_active:
        #     raise HTTPException(
        #         status_code=status.HTTP_403_FORBIDDEN,
        #         detail="Account is deactivated. Please contact support."
        #     )
        
        # Create access token using production schema
        token_data = {
            "sub": user.email,
            "user_id": str(user.id),  # Convert UUID to string
            "role": user.user_role  # Use production column name
        }
        access_token = create_access_token(token_data, SECRET_KEY, ALGORITHM)
        
        print(f"✅ User logged in: {user.email}")
        
        # Parse full_name back to firstName/lastName for frontend compatibility
        name_parts = user.full_name.split(' ', 1) if user.full_name else ['', '']
        first_name = name_parts[0] if len(name_parts) > 0 else ''
        last_name = name_parts[1] if len(name_parts) > 1 else ''
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": {
                "id": str(user.id),  # Convert UUID to string
                "email": user.email,
                "firstName": first_name,
                "lastName": last_name,
                "role": user.user_role  # Use production column name
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

# ----------------------------
# 2-Step Registration Endpoints (Frontend Compatibility)
# ----------------------------
@router.post("/auth/register/step1", tags=["auth-v2"])
async def register_step1(request: schemas.RegisterStep1Request, db: Session = Depends(get_db)):
    """
    Step 1: Validate email and basic info, create pending user
    """
    try:
        # Validate email format
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, request.email):
            raise HTTPException(
                status_code=400,
                detail="Invalid email format"
            )
        
        # Check if email already exists
        normalized_email = request.email.lower().strip()
        existing_user = db.query(models.User).filter(
            models.User.email == normalized_email
        ).first()
        
        if existing_user:
            print(f"❌ Step1 Debug: Email '{normalized_email}' found in database")
            print(f"   - Existing user ID: {existing_user.id}")
            raise HTTPException(
                status_code=400,
                detail="Email already registered"
            )
        
        print(f"✅ Step1 Debug: Email '{normalized_email}' is available")
        
        return {
            "success": True,
            "message": "Email validated successfully",
            "step": 1,
            "next_step": "/api/auth/register/step2"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Step 1 validation failed: {str(e)}"
        )

@router.post("/auth/register/step2", response_model=schemas.UserOut, tags=["auth-v2"])
async def register_step2(request: schemas.RegisterStep2Request, db: Session = Depends(get_db)):
    """
    Step 2: Complete registration with full user data
    """
    try:
        # Debug: Log incoming request data
        print(f"🔍 Step2 Debug: Incoming request data:")
        print(f"   - Email: '{request.email}'")
        print(f"   - Full name: '{request.full_name}'")
        print(f"   - User role: '{request.user_role}'")
        print(f"   - Company: '{request.company_name}'")
        
        # Validate required fields
        if not all([request.email, request.password, request.full_name]):
            print(f"❌ Step2 Debug: Missing required fields")
            raise HTTPException(
                status_code=400,
                detail="Email, password, and full name are required"
            )
        
        # Check email again (defensive programming)
        normalized_email = request.email.lower().strip()
        print(f"🔍 Step2 Debug: Checking email '{normalized_email}' in database...")
        
        existing_user = db.query(models.User).filter(
            models.User.email == normalized_email
        ).first()
        
        if existing_user:
            # Add debug info to understand why this is happening
            print(f"❌ Step2 Debug: Email '{normalized_email}' found in database")
            print(f"   - Existing user ID: {existing_user.id}")
            print(f"   - Existing user email: '{existing_user.email}'")
            print(f"   - Existing user created: {existing_user.created_at}")
            raise HTTPException(
                status_code=400,
                detail=f"Email already registered"
            )
        
        # Create new user with production schema fields
        print(f"🔐 Step2 Debug: About to hash password for '{normalized_email}'")
        try:
            hashed_password = get_password_hash(request.password)
            print(f"✅ Step2 Debug: Password hashed successfully")
        except Exception as hash_error:
            print(f"❌ Step2 Debug: Password hashing failed: {hash_error}")
            raise HTTPException(
                status_code=500,
                detail=f"Password hashing failed: {str(hash_error)}"
            )
        
        print(f"🔍 Step2 Debug: Creating user object...")
        
        # Map role to database-compatible values
        user_role = getattr(request, 'user_role', 'client')
        if user_role == 'customer':  # Handle legacy frontend values
            user_role = 'client'
        
        print(f"🔍 Step2 Debug: Using role '{user_role}' for database insert")
        
        db_user = models.User(
            email=request.email.lower().strip(),
            password_hash=hashed_password,
            full_name=request.full_name.strip(),
            user_role=user_role,
            company_name=getattr(request, 'company_name', None),
            tos_accepted_at=datetime.utcnow()
        )
        
        print(f"🔍 Step2 Debug: Adding user to database...")
        db.add(db_user)
        
        print(f"🔍 Step2 Debug: Committing transaction...")
        db.commit()
        
        print(f"🔍 Step2 Debug: Refreshing user object...")
        db.refresh(db_user)
        
        print(f"✅ Step2 Debug: User created successfully with ID: {db_user.id}")
        
        # Generate access token
        print(f"🔍 Step2 Debug: Generating access token...")
        access_token = create_access_token(data={"sub": db_user.email})
        
        print(f"✅ Step2 Debug: Registration completed successfully for '{normalized_email}'")
        
        return schemas.UserOut(
            id=str(db_user.id),
            email=db_user.email,
            full_name=db_user.full_name,
            user_role=db_user.user_role,
            company_name=db_user.company_name,
            access_token=access_token,
            created_at=db_user.created_at
        )
        
    except HTTPException:
        print(f"❌ Step2 Debug: HTTPException raised")
        raise
    except IntegrityError as ie:
        db.rollback()
        print(f"❌ Step2 Debug: IntegrityError - {ie}")
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )
    except Exception as e:
        db.rollback()
        print(f"❌ Step2 Debug: Unexpected error - {type(e).__name__}: {e}")
        import traceback
        print(f"❌ Step2 Debug: Traceback - {traceback.format_exc()}")
        raise HTTPException(
            status_code=500,
            detail=f"Registration failed: {str(e)}"
        )

# ----------------------------
# Email Verification Endpoints
# ----------------------------

from app.email_verification import email_verification_service
from pydantic import BaseModel

class EmailVerificationRequest(BaseModel):
    email: str

class EmailVerificationVerify(BaseModel):
    email: str
    code: str

@router.post("/auth/send-login-code", tags=["auth-v2"])
async def send_login_verification_code(
    request: EmailVerificationRequest,
    db: Session = Depends(get_db)
):
    """
    Send email verification code for login authentication
    """
    try:
        # Normalize email
        email = request.email.lower().strip()
        
        # Check if user exists
        user = db.query(models.User).filter(models.User.email == email).first()
        if not user:
            raise HTTPException(
                status_code=404,
                detail="User not found. Please check your email or register first."
            )
        
        # Send verification code
        success = await email_verification_service.send_login_code(
            db=db,
            email=email,
            user_agent=None,  # Could extract from request headers
            ip_address=None   # Could extract from request
        )
        
        if success:
            return {
                "success": True,
                "message": "Verification code sent to your email",
                "expires_in_minutes": 10
            }
        else:
            raise HTTPException(
                status_code=500,
                detail="Failed to send verification code. Please try again."
            )
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to send verification code: {str(e)}"
        )

@router.post("/auth/verify-login-code", tags=["auth-v2"])
async def verify_login_code(
    request: EmailVerificationVerify,
    db: Session = Depends(get_db)
):
    """
    Verify email code and complete login
    """
    try:
        # Normalize email
        email = request.email.lower().strip()
        
        # Verify the code
        success, message = await email_verification_service.verify_login_code(
            db=db,
            email=email,
            code=request.code
        )
        
        if not success:
            raise HTTPException(
                status_code=400,
                detail=message
            )
        
        # Get user details
        user = db.query(models.User).filter(models.User.email == email).first()
        if not user:
            raise HTTPException(
                status_code=404,
                detail="User not found"
            )
        
        # Generate access token
        access_token = create_access_token(data={"sub": user.email})
        
        return {
            "success": True,
            "message": "Login successful",
            "access_token": access_token,
            "token_type": "bearer",
            "user": {
                "id": str(user.id),
                "email": user.email,
                "full_name": user.full_name,
                "user_role": user.user_role
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Verification failed: {str(e)}"
        )
