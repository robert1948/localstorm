#!/usr/bin/env python3
"""
Heroku One-Time Migration Script
This script can be run as a one-time task on Heroku to migrate the database
Usage: heroku run python scripts/heroku_one_time_migration.py --app YOUR_APP_NAME
"""
import os
import sys
import psycopg2
from urllib.parse import urlparse

def run_migration():
    """Run the email verification migration on Heroku"""
    
    print("🚀 Starting Heroku PostgreSQL Migration...")
    
    # Get database URL from environment
    DATABASE_URL = os.environ.get('DATABASE_URL')
    if not DATABASE_URL:
        print("❌ DATABASE_URL environment variable not found")
        return False
    
    print("🔗 Connecting to Heroku PostgreSQL...")
    
    try:
        # Connect to the database
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()
        
        print("✅ Connected to database successfully")
        
        # Check if table already exists
        cursor.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_schema = 'public' 
                AND table_name = 'verification_codes'
            );
        """)
        
        table_exists = cursor.fetchone()[0]
        
        if table_exists:
            print("⚠️  verification_codes table already exists")
            print("🔍 Checking table structure...")
            
            cursor.execute("""
                SELECT column_name, data_type 
                FROM information_schema.columns 
                WHERE table_name = 'verification_codes'
                ORDER BY ordinal_position;
            """)
            
            columns = cursor.fetchall()
            print("📊 Current table structure:")
            for column_name, data_type in columns:
                print(f"  - {column_name}: {data_type}")
            
            return True
        
        print("📋 Creating verification_codes table...")
        
        # Create the verification_codes table
        cursor.execute("""
            CREATE TABLE verification_codes (
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
        """)
        
        print("✅ Created verification_codes table")
        
        # Create indexes
        print("🔍 Creating database indexes...")
        
        cursor.execute("""
            CREATE INDEX idx_verification_codes_email 
            ON verification_codes (email);
        """)
        
        cursor.execute("""
            CREATE INDEX idx_verification_codes_active 
            ON verification_codes (email, purpose, is_used, expires_at);
        """)
        
        print("✅ Created database indexes")
        
        # Commit the changes
        conn.commit()
        
        # Verify the table structure
        cursor.execute("""
            SELECT column_name, data_type 
            FROM information_schema.columns 
            WHERE table_name = 'verification_codes'
            ORDER BY ordinal_position;
        """)
        
        columns = cursor.fetchall()
        print("\n📊 verification_codes table structure:")
        for column_name, data_type in columns:
            print(f"  - {column_name}: {data_type}")
        
        print("\n✅ Migration completed successfully!")
        print("🎉 Email verification system is ready!")
        
        return True
        
    except psycopg2.Error as e:
        print(f"❌ Database error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()
        print("🔌 Database connection closed")

if __name__ == "__main__":
    print("🗄️  Heroku PostgreSQL Email Verification Migration")
    print("=" * 50)
    
    success = run_migration()
    
    if success:
        print("\n🚀 Migration Status: SUCCESS")
        print("📊 The email verification system is now available")
        print("🔗 API endpoints ready: /auth/send-login-code and /auth/verify-login-code")
    else:
        print("\n❌ Migration Status: FAILED")
        print("🔧 Please check the error messages above")
    
    sys.exit(0 if success else 1)
