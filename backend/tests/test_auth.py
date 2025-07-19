"""
Unit tests for CapeControl authentication system
"""
import pytest
import os
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Set test environment variables before importing app modules
os.environ["SECRET_KEY"] = "test-secret-key-for-jwt-tokens"
os.environ["DATABASE_URL"] = "sqlite:///./test.db"
os.environ["DEBUG"] = "True"

from app.main import app
from app.database import get_db, Base

# Create test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

class TestAuth:
    """Test authentication endpoints"""
    
    def test_health_endpoint(self):
        """Test health check endpoint"""
        response = client.get("/api/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "database_connected" in data
    
    def test_email_validation_available(self):
        """Test email validation for available email"""
        response = client.get("/api/auth/v2/validate-email?email=test@example.com")
        assert response.status_code == 200
        data = response.json()
        assert data["available"] == True
    
    def test_password_validation_weak(self):
        """Test password validation for weak password"""
        response = client.post("/api/auth/v2/validate-password", 
                             json={"password": "123"})
        assert response.status_code == 200
        data = response.json()
        assert data["valid"] == False
        assert "doesn't meet requirements" in data["message"].lower()
    
    def test_password_validation_strong(self):
        """Test password validation for strong password"""
        response = client.post("/api/auth/v2/validate-password", 
                             json={"password": "StrongPassword123!"})
        assert response.status_code == 200
        data = response.json()
        assert data["valid"] == True
    
    def test_registration_step1_valid(self):
        """Test step 1 registration with valid data"""
        user_data = {
            "email": "newuser@example.com",
            "password": "StrongPassword123!",
            "full_name": "Test User",
            "user_role": "customer"
        }
        response = client.post("/api/auth/register/step1", json=user_data)
        assert response.status_code == 200
        data = response.json()
        assert data["success"] == True
        assert data["step"] == 1
        assert "next_step" in data

    def test_registration_duplicate_email(self):
        """Test registration with duplicate email"""
        user_data = {
            "email": "duplicate@example.com",
            "password": "StrongPassword123!",
            "full_name": "Test User",
            "user_role": "client",
            "tos_accepted": True
        }
        # First registration - should succeed
        response1 = client.post("/api/auth/v2/register", json=user_data)
        assert response1.status_code == 200
        
        # Second registration should fail
        response2 = client.post("/api/auth/v2/register", json=user_data)
        assert response2.status_code == 409
        assert "already registered" in response2.json()["detail"].lower()

class TestCapeAI:
    """Test CapeAI system components"""
    
    def test_onboarding_step_tracking(self):
        """Test onboarding progress tracking"""
        # This would test the frontend onboarding system
        # For now, we can test that the user creation includes onboarding fields
        pass

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
