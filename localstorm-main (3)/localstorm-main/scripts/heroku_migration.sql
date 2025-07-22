-- Heroku PostgreSQL Email Verification Migration
-- Run these commands in your PostgreSQL client

-- Create verification_codes table

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


-- Create indexes for performance  

CREATE INDEX IF NOT EXISTS idx_verification_codes_email 
ON verification_codes (email);

CREATE INDEX IF NOT EXISTS idx_verification_codes_active 
ON verification_codes (email, purpose, is_used, expires_at);


-- Verify table structure

SELECT column_name, data_type, is_nullable
FROM information_schema.columns 
WHERE table_name = 'verification_codes'
ORDER BY ordinal_position;


-- Test the table
INSERT INTO verification_codes (email, code, purpose, expires_at) 
VALUES ('test@example.com', '123456', 'login', NOW() + INTERVAL '10 minutes');

SELECT * FROM verification_codes WHERE email = 'test@example.com';

-- Clean up test data
DELETE FROM verification_codes WHERE email = 'test@example.com';
