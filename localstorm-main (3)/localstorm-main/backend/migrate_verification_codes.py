"""
Database migration to add verification_codes table for email authentication
"""

from sqlalchemy import text
from app.database import engine

def upgrade():
    """Add verification_codes table"""
    with engine.connect() as connection:
        # Create verification_codes table (PostgreSQL syntax)
        connection.execute(text("""
            CREATE TABLE IF NOT EXISTS verification_codes (
                id SERIAL PRIMARY KEY,
                email VARCHAR NOT NULL,
                code VARCHAR(6) NOT NULL,
                purpose VARCHAR NOT NULL,
                created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                expires_at TIMESTAMP NOT NULL,
                used_at TIMESTAMP NULL,
                is_used BOOLEAN NOT NULL DEFAULT FALSE,
                attempts INTEGER NOT NULL DEFAULT 0,
                user_agent VARCHAR NULL,
                ip_address VARCHAR NULL
            )
        """))
        
        # Create indexes for better performance
        connection.execute(text("""
            CREATE INDEX IF NOT EXISTS idx_verification_codes_email 
            ON verification_codes(email)
        """))
        
        connection.execute(text("""
            CREATE INDEX IF NOT EXISTS idx_verification_codes_purpose 
            ON verification_codes(purpose)
        """))
        
        connection.execute(text("""
            CREATE INDEX IF NOT EXISTS idx_verification_codes_expires_at 
            ON verification_codes(expires_at)
        """))
        
        connection.commit()
        print("✅ Added verification_codes table and indexes")

if __name__ == "__main__":
    upgrade()
