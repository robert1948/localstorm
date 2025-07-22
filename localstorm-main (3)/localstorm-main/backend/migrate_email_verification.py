"""
Database migration to add email verification codes table
Run this script to update the PostgreSQL database with email verification functionality
"""
import os
import sys
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

# Add the parent directory to the path to import app modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import DATABASE_URL, engine
from app.email_verification import VerificationCode, Base

def create_verification_codes_table():
    """Create the verification_codes table in PostgreSQL"""
    
    print("Creating verification_codes table...")
    
    # DDL for PostgreSQL
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS verification_codes (
        id SERIAL PRIMARY KEY,
        email VARCHAR(255) NOT NULL,
        code VARCHAR(6) NOT NULL,
        purpose VARCHAR(50) NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        expires_at TIMESTAMP NOT NULL,
        used_at TIMESTAMP NULL,
        is_used BOOLEAN DEFAULT FALSE,
        attempts INTEGER DEFAULT 0,
        user_agent TEXT NULL,
        ip_address VARCHAR(45) NULL
    );
    """
    
    # Create index on email for faster lookups
    create_index_sql = """
    CREATE INDEX IF NOT EXISTS idx_verification_codes_email 
    ON verification_codes (email);
    """
    
    # Create composite index for active codes
    create_composite_index_sql = """
    CREATE INDEX IF NOT EXISTS idx_verification_codes_active 
    ON verification_codes (email, purpose, is_used, expires_at);
    """
    
    try:
        with engine.connect() as connection:
            # Execute the table creation
            connection.execute(text(create_table_sql))
            print("✅ verification_codes table created successfully")
            
            # Create indexes
            connection.execute(text(create_index_sql))
            print("✅ Email index created successfully")
            
            connection.execute(text(create_composite_index_sql))
            print("✅ Composite index created successfully")
            
            # Commit the transaction
            connection.commit()
            
        print("\n🎉 Database migration completed successfully!")
        print(f"📊 Connected to: {DATABASE_URL[:20]}...")
        
    except Exception as e:
        print(f"❌ Migration failed: {str(e)}")
        return False
    
    return True

def verify_table_creation():
    """Verify that the table was created correctly"""
    
    print("\nVerifying table creation...")
    
    verify_sql = """
    SELECT column_name, data_type, is_nullable 
    FROM information_schema.columns 
    WHERE table_name = 'verification_codes'
    ORDER BY ordinal_position;
    """
    
    try:
        with engine.connect() as connection:
            result = connection.execute(text(verify_sql))
            columns = result.fetchall()
            
            if columns:
                print("✅ Table verification successful!")
                print("\nTable structure:")
                print("-" * 50)
                for column in columns:
                    print(f"  {column[0]:15} | {column[1]:15} | Nullable: {column[2]}")
                print("-" * 50)
                return True
            else:
                print("❌ Table not found!")
                return False
                
    except Exception as e:
        print(f"❌ Verification failed: {str(e)}")
        return False

if __name__ == "__main__":
    print("🚀 Starting database migration for email verification...")
    print(f"🔗 Database URL: {DATABASE_URL[:30]}...")
    
    # Run migration
    if create_verification_codes_table():
        verify_table_creation()
        print("\n✨ Migration complete! Email verification is now ready.")
    else:
        print("\n💥 Migration failed! Please check the error messages above.")
        sys.exit(1)
