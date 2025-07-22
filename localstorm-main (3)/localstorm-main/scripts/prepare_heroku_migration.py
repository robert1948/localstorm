"""
Heroku PostgreSQL Migration using SQL statements
This script can be run in environments with proper network access to Heroku
"""
import os
import sys

# SQL statements for email verification migration
CREATE_TABLE_SQL = """
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

CREATE_INDEXES_SQL = """
CREATE INDEX IF NOT EXISTS idx_verification_codes_email 
ON verification_codes (email);

CREATE INDEX IF NOT EXISTS idx_verification_codes_active 
ON verification_codes (email, purpose, is_used, expires_at);
"""

VERIFY_TABLE_SQL = """
SELECT column_name, data_type, is_nullable
FROM information_schema.columns 
WHERE table_name = 'verification_codes'
ORDER BY ordinal_position;
"""

def print_migration_instructions():
    """Print instructions for manual migration"""
    print("🚀 Heroku PostgreSQL Email Verification Migration")
    print("=" * 55)
    print()
    print("📋 MANUAL MIGRATION INSTRUCTIONS:")
    print("=" * 35)
    print()
    print("1. 🌐 Run this from a machine with internet access (not dev container)")
    print("2. 🔧 Install PostgreSQL client: `brew install postgresql` (Mac) or `apt-get install postgresql-client` (Linux)")
    print("3. 🗄️  Connect to Heroku database using psql:")
    print()
    print("   psql postgresql://u8h1en29mru00:p3020c7560854b178b598d2993a2b91173972e98a202f19c9ba981e3bbd8@c7jla3ha5puqsf.cluster-czrs8kj4isg6.us-east-1.rds.amazonaws.com:5432/d5h1tdp6nrlcj8")
    print()
    print("4. 📝 Run the following SQL commands:")
    print()
    print("   -- Create verification_codes table")
    print("   " + CREATE_TABLE_SQL.strip())
    print()
    print("   -- Create indexes for performance")
    print("   " + CREATE_INDEXES_SQL.strip())
    print()
    print("5. ✅ Verify table creation:")
    print("   \\d verification_codes")
    print()
    print("🔗 ALTERNATIVE - Use Heroku CLI:")
    print("=" * 35)
    print()
    print("1. 📱 Install Heroku CLI: https://devcenter.heroku.com/articles/heroku-cli")
    print("2. 🔐 Login: `heroku login`") 
    print("3. 🗄️  Connect to database: `heroku pg:psql --app YOUR_APP_NAME`")
    print("4. 📝 Run the SQL commands above")
    print()
    print("🎯 WHAT THIS MIGRATION DOES:")
    print("=" * 30)
    print("• Creates verification_codes table for email authentication")
    print("• Adds indexes for optimal query performance")
    print("• Supports 6-digit verification codes with expiry")
    print("• Tracks usage attempts and prevents reuse")
    print("• Compatible with the new email verification API endpoints")
    print()

def save_sql_file():
    """Save SQL commands to a file for easy execution"""
    sql_content = f"""-- Heroku PostgreSQL Email Verification Migration
-- Run these commands in your PostgreSQL client

-- Create verification_codes table
{CREATE_TABLE_SQL}

-- Create indexes for performance  
{CREATE_INDEXES_SQL}

-- Verify table structure
{VERIFY_TABLE_SQL}

-- Test the table
INSERT INTO verification_codes (email, code, purpose, expires_at) 
VALUES ('test@example.com', '123456', 'login', NOW() + INTERVAL '10 minutes');

SELECT * FROM verification_codes WHERE email = 'test@example.com';

-- Clean up test data
DELETE FROM verification_codes WHERE email = 'test@example.com';
"""

    with open('/workspaces/localstorm/scripts/heroku_migration.sql', 'w') as f:
        f.write(sql_content)
    
    print("💾 SQL migration file saved to: scripts/heroku_migration.sql")
    print("📋 You can run this file with: psql DATABASE_URL -f scripts/heroku_migration.sql")

if __name__ == "__main__":
    print_migration_instructions()
    print()
    save_sql_file()
    print()
    print("🚀 Migration preparation complete!")
    print("📱 Run the instructions above to update your Heroku PostgreSQL database")
