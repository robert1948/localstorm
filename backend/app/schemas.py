from pydantic import BaseModel, EmailStr

# ----------------------------
# Schema: User Registration
# ----------------------------
class UserCreate(BaseModel):
    """
    Schema for creating a new user.
    """
    email: EmailStr
    password: str

    class Config:
        from_attributes = True


# ----------------------------
# Schema: User Login (JSON input)
# ----------------------------
class LoginInput(BaseModel):
    """
    Schema for user login via JSON.
    """
    email: EmailStr
    password: str


# ----------------------------
# Schema: Public User Info (safe output)
# ----------------------------
class UserOut(BaseModel):
    """
    Schema for returning user information (excluding sensitive data).
    """
    id: int
    email: EmailStr

    class Config:
        from_attributes = True
