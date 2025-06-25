from sqlalchemy import Column, Integer, String
from app.database import Base  # Updated import for new structure

class User(Base):
    """
    SQLAlchemy model for the users table.
    Stores user credentials and authentication details.
    """
    __tablename__ = "users"  # Correct attribute name

    id = Column(Integer, primary_key=True, index=True)  # Unique user ID
    email = Column(String(255), unique=True, index=True)  # User email, must be unique
    hashed_password = Column(String(255))  # Hashed user password