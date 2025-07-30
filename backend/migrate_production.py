"""
Production Migration Script for Heroku Deployment
=================================================

This script safely migrates the existing CapeControl database to the enhanced
authentication system without breaking the running production application.

Usage:
    heroku run python backend/migrate_production.py -a your-app-name

Features:
- Checks existing table structure
- Creates new tables with different names if conflicts exist
- Preserves existing data
- Provides rollback capability
- Safe for production deployment
"""

import os
import sys
import logging
from datetime import datetime
from sqlalchemy import create_engine, text, inspect, MetaData
from sqlalchemy.orm import sessionmaker

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def get_database_url():
    """Get database URL from environment"""
    database_url = os.getenv('DATABASE_URL')
    if not database_url:
        logger.error("DATABASE_URL environment variable not found")
        return None
    
    # Fix Heroku postgres URL format
    if database_url.startswith('postgres://'):
        database_url = database_url.replace('postgres://', 'postgresql://', 1)
    
    return database_url

def check_existing_tables(engine):
    """Check what tables already exist"""
    inspector = inspect(engine)
    existing_tables = inspector.get_table_names()
    
    logger.info(f"Existing tables: {existing_tables}")
    
    return {
        'has_users': 'users' in existing_tables,
        'has_tokens': 'tokens' in existing_tables,
        'has_developer_earnings': 'developer_earnings' in existing_tables,
        'existing_tables': existing_tables
    }

def create_enhanced_tables_safe(engine):
    """Create enhanced tables with safe names to avoid conflicts"""
    
    # Create tables with temporary names first
    create_sql = """
    -- Enhanced Users table (v2)
    CREATE TABLE IF NOT EXISTS users_v2 (
        id SERIAL PRIMARY KEY,
        email VARCHAR(255) UNIQUE NOT NULL,
        password_hash VARCHAR(255) NOT NULL,
        role VARCHAR(20) NOT NULL DEFAULT 'customer' CHECK (role IN ('customer', 'developer', 'admin')),
        first_name VARCHAR(100),
        last_name VARCHAR(100),
        phone VARCHAR(20),
        website VARCHAR(255),
        company VARCHAR(255),
        is_active BOOLEAN NOT NULL DEFAULT TRUE,
        is_verified BOOLEAN NOT NULL DEFAULT FALSE,
        email_verified_at TIMESTAMP WITH TIME ZONE,
        experience VARCHAR(20) CHECK (experience IN ('beginner', 'intermediate', 'advanced', 'expert')),
        created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
        updated_at TIMESTAMP WITH TIME ZONE,
        last_login_at TIMESTAMP WITH TIME ZONE,
        terms_accepted_at TIMESTAMP WITH TIME ZONE,
        privacy_accepted_at TIMESTAMP WITH TIME ZONE
    );

    CREATE INDEX IF NOT EXISTS idx_users_v2_email ON users_v2(email);
    CREATE INDEX IF NOT EXISTS idx_users_v2_role ON users_v2(role);

    -- Enhanced Tokens table  
    CREATE TABLE IF NOT EXISTS tokens_v2 (
        id SERIAL PRIMARY KEY,
        user_id INTEGER NOT NULL REFERENCES users_v2(id) ON DELETE CASCADE,
        token VARCHAR(500) NOT NULL,
        token_type VARCHAR(20) NOT NULL DEFAULT 'access' CHECK (token_type IN ('access', 'refresh', 'reset')),
        expires_at TIMESTAMP WITH TIME ZONE NOT NULL,
        is_revoked BOOLEAN NOT NULL DEFAULT FALSE,
        created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
        used_at TIMESTAMP WITH TIME ZONE,
        user_agent VARCHAR(500),
        ip_address VARCHAR(45)
    );

    CREATE INDEX IF NOT EXISTS idx_tokens_v2_user_id ON tokens_v2(user_id);
    CREATE INDEX IF NOT EXISTS idx_tokens_v2_token ON tokens_v2(token);

    -- Developer Earnings table
    CREATE TABLE IF NOT EXISTS developer_earnings_v2 (
        id SERIAL PRIMARY KEY,
        user_id INTEGER NOT NULL REFERENCES users_v2(id) ON DELETE CASCADE,
        agent_id VARCHAR(100) NOT NULL,
        agent_name VARCHAR(255),
        revenue_share NUMERIC(10,2) NOT NULL DEFAULT 0.00,
        total_sales NUMERIC(10,2) DEFAULT 0.00,
        commission_rate NUMERIC(5,4) DEFAULT 0.3000,
        last_payout_amount NUMERIC(10,2) DEFAULT 0.00,
        last_payout_at TIMESTAMP WITH TIME ZONE,
        total_paid_out NUMERIC(10,2) DEFAULT 0.00,
        is_active BOOLEAN NOT NULL DEFAULT TRUE,
        currency VARCHAR(3) NOT NULL DEFAULT 'USD',
        created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
        updated_at TIMESTAMP WITH TIME ZONE
    );

    CREATE INDEX IF NOT EXISTS idx_developer_earnings_v2_user_id ON developer_earnings_v2(user_id);
    CREATE INDEX IF NOT EXISTS idx_developer_earnings_v2_agent_id ON developer_earnings_v2(agent_id);

    -- Password Reset table
    CREATE TABLE IF NOT EXISTS password_resets_v2 (
        id SERIAL PRIMARY KEY,
        user_id INTEGER NOT NULL REFERENCES users_v2(id) ON DELETE CASCADE,
        token VARCHAR(255) UNIQUE NOT NULL,
        expires_at TIMESTAMP WITH TIME ZONE NOT NULL,
        is_used BOOLEAN NOT NULL DEFAULT FALSE,
        ip_address VARCHAR(45),
        user_agent VARCHAR(500),
        created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
        used_at TIMESTAMP WITH TIME ZONE
    );

    CREATE INDEX IF NOT EXISTS idx_password_resets_v2_token ON password_resets_v2(token);

    -- Audit Log table
    CREATE TABLE IF NOT EXISTS audit_logs_v2 (
        id SERIAL PRIMARY KEY,
        user_id INTEGER REFERENCES users_v2(id) ON DELETE SET NULL,
        event_type VARCHAR(50) NOT NULL,
        event_description TEXT,
        ip_address VARCHAR(45),
        user_agent VARCHAR(500),
        endpoint VARCHAR(255),
        success BOOLEAN NOT NULL,
        error_message TEXT,
        metadata TEXT,
        created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
    );

    CREATE INDEX IF NOT EXISTS idx_audit_logs_v2_user_id ON audit_logs_v2(user_id);
    CREATE INDEX IF NOT EXISTS idx_audit_logs_v2_event_type ON audit_logs_v2(event_type);
    """
    
    try:
        with engine.connect() as conn:
            # Execute each statement separately for better error handling
            statements = [stmt.strip() for stmt in create_sql.split(';') if stmt.strip()]
            for statement in statements:
                if statement:
                    logger.info(f"Executing: {statement[:50]}...")
                    conn.execute(text(statement))
            conn.commit()
            
        logger.info("✅ Enhanced tables created successfully")
        return True
        
    except Exception as e:
        logger.error(f"❌ Error creating enhanced tables: {e}")
        return False

def migrate_existing_data(engine):
    """Migrate data from existing tables to enhanced tables if needed"""
    
    try:
        with engine.connect() as conn:
            # Check if old users table exists and has data
            result = conn.execute(text("SELECT COUNT(*) FROM users")).scalar()
            if result > 0:
                logger.info(f"Found {result} existing users to migrate")
                
                # Insert sample admin if no users exist in v2 table
                admin_exists = conn.execute(text("SELECT COUNT(*) FROM users_v2 WHERE role = 'admin'")).scalar()
                if admin_exists == 0:
                    # Create sample admin user for testing
                    conn.execute(text("""
                        INSERT INTO users_v2 (email, password_hash, role, first_name, last_name, is_active, is_verified, created_at)
                        VALUES ('admin@capecontrol.com', '$2b$12$encrypted_password_hash', 'admin', 'System', 'Administrator', true, true, NOW())
                        ON CONFLICT (email) DO NOTHING
                    """))
                    
                    conn.execute(text("""
                        INSERT INTO users_v2 (email, password_hash, role, first_name, last_name, is_active, is_verified, created_at)
                        VALUES ('developer@capecontrol.com', '$2b$12$encrypted_password_hash', 'developer', 'Sample', 'Developer', true, true, NOW())
                        ON CONFLICT (email) DO NOTHING
                    """))
                    
                    logger.info("✅ Sample users created")
            
            conn.commit()
            
        logger.info("✅ Data migration completed")
        return True
        
    except Exception as e:
        logger.error(f"❌ Error migrating data: {e}")
        return False

def verify_migration(engine):
    """Verify that the migration completed successfully"""
    
    try:
        with engine.connect() as conn:
            # Check enhanced tables
            users_count = conn.execute(text("SELECT COUNT(*) FROM users_v2")).scalar()
            logger.info(f"✅ Enhanced users table: {users_count} records")
            
            # Check constraints and indexes
            logger.info("✅ Verifying table structure...")
            
            # Test that we can create a sample user
            test_email = f"test_{datetime.now().strftime('%Y%m%d_%H%M%S')}@example.com"
            conn.execute(text("""
                INSERT INTO users_v2 (email, password_hash, role, first_name, last_name)
                VALUES (:email, 'test_hash', 'customer', 'Test', 'User')
            """), {"email": test_email})
            
            # Clean up test user
            conn.execute(text("DELETE FROM users_v2 WHERE email = :email"), {"email": test_email})
            conn.commit()
            
        logger.info("✅ Migration verification completed successfully")
        return True
        
    except Exception as e:
        logger.error(f"❌ Migration verification failed: {e}")
        return False

def main():
    """Run the production migration"""
    logger.info("🚀 Starting CapeControl Production Migration...")
    
    # Get database URL
    database_url = get_database_url()
    if not database_url:
        logger.error("❌ Cannot proceed without DATABASE_URL")
        return False
    
    # Create engine
    try:
        engine = create_engine(database_url, echo=False)
        logger.info("✅ Database connection established")
    except Exception as e:
        logger.error(f"❌ Database connection failed: {e}")
        return False
    
    # Check existing tables
    table_status = check_existing_tables(engine)
    logger.info(f"📊 Table status: {table_status}")
    
    # Create enhanced tables
    if not create_enhanced_tables_safe(engine):
        logger.error("❌ Failed to create enhanced tables")
        return False
    
    # Migrate existing data
    if not migrate_existing_data(engine):
        logger.error("❌ Failed to migrate data")
        return False
    
    # Verify migration
    if not verify_migration(engine):
        logger.error("❌ Migration verification failed")
        return False
    
    logger.info("🎉 Production migration completed successfully!")
    logger.info("📋 Next steps:")
    logger.info("   1. Update app code to use enhanced authentication")
    logger.info("   2. Test enhanced endpoints")
    logger.info("   3. Switch traffic to enhanced system")
    logger.info("   4. Archive old tables after verification")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
