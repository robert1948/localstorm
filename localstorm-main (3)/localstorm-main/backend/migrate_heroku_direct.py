#!/usr/bin/env python3
"""
Direct Heroku PostgreSQL migration for email verification
This script connects directly to Heroku PostgreSQL and creates the verification_codes table
"""
import psycopg2
import os
import sys

def migrate_heroku_database():
    """Migrate Heroku PostgreSQL database directly"""
    
    # Heroku PostgreSQL connection details from the provided URL
    DATABASE_URL = "postgresql://u8h1en29mru00:p3020c7560854b178b598d2993a2b91173972e98a202f19c9ba981e3bbd8@c7jla3ha5puqsf.cluster-czrs8kj4isg6.us-east-1.rds.amazonaws.com:5432/d5h1tdp6nrlcj8"
    
    print("🚀 Starting Heroku PostgreSQL migration...")
    print("🔗 Connecting to Heroku database...")
    
    try:
        # Connect to the PostgreSQL database
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()
        
        print("✅ Connected to Heroku PostgreSQL database")
        
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
            return True
            
        print("📋 Creating verification_codes table...")
        
        # Create the verification_codes table
        create_table_sql = """
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
        """
        
        cursor.execute(create_table_sql)
        print("✅ Created verification_codes table")
        
        # Create indexes for performance
        print("🔍 Creating database indexes...")
        
        # Index on email for faster lookups
        cursor.execute("""
            CREATE INDEX idx_verification_codes_email 
            ON verification_codes (email);
        """)
        
        # Composite index for active codes
        cursor.execute("""
            CREATE INDEX idx_verification_codes_active 
            ON verification_codes (email, purpose, is_used, expires_at);
        """)
        
        print("✅ Created database indexes")
        
        # Commit the changes
        conn.commit()
        print("✅ Migration completed successfully!")
        
        # Verify the table was created
        cursor.execute("""
            SELECT column_name, data_type 
            FROM information_schema.columns 
            WHERE table_name = 'verification_codes'
            ORDER BY ordinal_position;
        """)
        
        columns = cursor.fetchall()
        print("\n📊 Verification codes table structure:")
        for column_name, data_type in columns:
            print(f"  - {column_name}: {data_type}")
            
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
    success = migrate_heroku_database()
    sys.exit(0 if success else 1)
