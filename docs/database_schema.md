# CapeControl Authentication Architecture
## Secure, Scalable Database Schema Design

### Overview
This document outlines the complete database schema for CapeControl's secure authentication system, designed for scalability, security, and developer revenue tracking.

### Core Design Principles
- **Security First**: Password hashing, JWT tokens, audit logging
- **Scalability**: Indexed fields, proper foreign keys, efficient queries
- **Developer Focus**: Revenue tracking, commission management
- **Compliance**: Audit trails, data retention, privacy controls

---

## Database Schema

### 1. Users Table
The core users table with enhanced security and role management.

```sql
CREATE TABLE users (
    -- Primary identification
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    
    -- Role-based access control
    role VARCHAR(20) NOT NULL DEFAULT 'customer' CHECK (role IN ('customer', 'developer', 'admin')),
    
    -- Profile information
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    phone VARCHAR(20),
    website VARCHAR(255),
    company VARCHAR(255),
    
    -- Account status and verification
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    is_verified BOOLEAN NOT NULL DEFAULT FALSE,
    email_verified_at TIMESTAMP WITH TIME ZONE,
    
    -- Experience level
    experience VARCHAR(20) CHECK (experience IN ('beginner', 'intermediate', 'advanced', 'expert')),
    
    -- Audit fields
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE,
    last_login_at TIMESTAMP WITH TIME ZONE,
    
    -- Terms and privacy
    terms_accepted_at TIMESTAMP WITH TIME ZONE,
    privacy_accepted_at TIMESTAMP WITH TIME ZONE
);

-- Indexes for performance
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_role ON users(role);
CREATE INDEX idx_users_created_at ON users(created_at);
```

**Key Features:**
- Unique, indexed email for fast authentication
- Role-based access control (customer/developer/admin)
- Account verification and status tracking
- Audit timestamps for compliance
- Privacy and terms acceptance tracking

### 2. Tokens Table
JWT and session management with security tracking.

```sql
CREATE TABLE tokens (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    
    -- Token details
    token VARCHAR(500) NOT NULL,
    token_type VARCHAR(20) NOT NULL DEFAULT 'access' CHECK (token_type IN ('access', 'refresh', 'reset')),
    
    -- Expiration and status
    expires_at TIMESTAMP WITH TIME ZONE NOT NULL,
    is_revoked BOOLEAN NOT NULL DEFAULT FALSE,
    
    -- Audit fields
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    used_at TIMESTAMP WITH TIME ZONE,
    
    -- Device/session tracking
    user_agent VARCHAR(500),
    ip_address VARCHAR(45)
);

-- Indexes for performance
CREATE INDEX idx_tokens_user_id ON tokens(user_id);
CREATE INDEX idx_tokens_token ON tokens(token);
CREATE INDEX idx_tokens_expires_at ON tokens(expires_at);
```

**Key Features:**
- Support for access, refresh, and reset tokens
- Automatic expiration handling
- Device and IP tracking for security
- Token revocation capability

### 3. Developer Earnings Table
Revenue tracking and commission management for developers.

```sql
CREATE TABLE developer_earnings (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    
    -- AI Agent identification
    agent_id VARCHAR(100) NOT NULL,
    agent_name VARCHAR(255),
    
    -- Revenue details
    revenue_share DECIMAL(10,2) NOT NULL DEFAULT 0.00,
    total_sales DECIMAL(10,2) DEFAULT 0.00,
    commission_rate DECIMAL(5,4) DEFAULT 0.3000, -- 30% default
    
    -- Payment tracking
    last_payout_amount DECIMAL(10,2) DEFAULT 0.00,
    last_payout_at TIMESTAMP WITH TIME ZONE,
    total_paid_out DECIMAL(10,2) DEFAULT 0.00,
    
    -- Status and metadata
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    currency VARCHAR(3) NOT NULL DEFAULT 'USD',
    
    -- Audit fields
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE
);

-- Indexes for performance
CREATE INDEX idx_developer_earnings_user_id ON developer_earnings(user_id);
CREATE INDEX idx_developer_earnings_agent_id ON developer_earnings(agent_id);
CREATE INDEX idx_developer_earnings_created_at ON developer_earnings(created_at);
```

**Key Features:**
- Links developers to their AI agents
- Tracks revenue share and commission rates
- Payment history and status
- Multi-currency support

### 4. Password Reset Table
Secure password reset workflow.

```sql
CREATE TABLE password_resets (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    
    -- Reset token details
    token VARCHAR(255) UNIQUE NOT NULL,
    expires_at TIMESTAMP WITH TIME ZONE NOT NULL,
    is_used BOOLEAN NOT NULL DEFAULT FALSE,
    
    -- Security tracking
    ip_address VARCHAR(45),
    user_agent VARCHAR(500),
    
    -- Audit fields
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    used_at TIMESTAMP WITH TIME ZONE
);

-- Indexes for performance
CREATE INDEX idx_password_resets_token ON password_resets(token);
CREATE INDEX idx_password_resets_user_id ON password_resets(user_id);
```

**Key Features:**
- Time-limited, single-use tokens
- IP and device tracking for security
- Automatic cleanup of expired tokens

### 5. Audit Log Table
Security and compliance audit trail.

```sql
CREATE TABLE audit_logs (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
    
    -- Event details
    event_type VARCHAR(50) NOT NULL,
    event_description TEXT,
    
    -- Request details
    ip_address VARCHAR(45),
    user_agent VARCHAR(500),
    endpoint VARCHAR(255),
    
    -- Status and metadata
    success BOOLEAN NOT NULL,
    error_message TEXT,
    metadata TEXT, -- JSON string for additional data
    
    -- Timestamp
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
);

-- Indexes for performance
CREATE INDEX idx_audit_logs_user_id ON audit_logs(user_id);
CREATE INDEX idx_audit_logs_event_type ON audit_logs(event_type);
CREATE INDEX idx_audit_logs_created_at ON audit_logs(created_at);
CREATE INDEX idx_audit_logs_success ON audit_logs(success);
```

**Key Features:**
- Comprehensive event logging
- Security monitoring and alerting
- Compliance reporting
- Performance metrics

---

## Relationships and Constraints

### Entity Relationships
```
Users (1) ──── (N) Tokens
Users (1) ──── (N) Developer_Earnings
Users (1) ──── (N) Password_Resets
Users (1) ──── (N) Audit_Logs
```

### Security Constraints
- All passwords are hashed using bcrypt with salt
- JWTs are signed with secure secrets
- All foreign keys have CASCADE or SET NULL for data integrity
- Sensitive operations are logged in audit_logs

### Performance Optimizations
- Strategic indexing on frequently queried fields
- Proper data types and constraints
- Automatic cleanup procedures for expired tokens

---

## Security Features

### Authentication Security
- **Password Hashing**: bcrypt with salts
- **JWT Tokens**: Signed with HS256, configurable expiration
- **Token Revocation**: Ability to invalidate tokens
- **Session Tracking**: IP and device monitoring

### Access Control
- **Role-Based Access**: Customer, Developer, Admin roles
- **Resource Protection**: JWT-protected endpoints
- **Permission Checks**: Role-specific access controls

### Audit and Compliance
- **Event Logging**: All security events tracked
- **Data Retention**: Configurable log retention
- **Privacy Controls**: GDPR-compliant data handling

---

## Scalability Considerations

### Database Performance
- Indexed queries for fast authentication
- Efficient joins with proper foreign keys
- Automatic cleanup of expired data

### Horizontal Scaling
- Stateless JWT tokens (no server-side sessions)
- Database-agnostic design
- Cloud-ready architecture

### Developer Revenue Scale
- Efficient earnings aggregation
- Support for multiple payment processors
- Real-time revenue tracking

---

## Migration Strategy

### Phase 1: Core Authentication
1. Deploy users and tokens tables
2. Implement JWT authentication
3. Basic role-based access

### Phase 2: Developer Features
1. Add developer_earnings table
2. Implement revenue tracking
3. Payment integration

### Phase 3: Security & Compliance
1. Add audit_logs table
2. Implement password reset flow
3. Enhanced security monitoring

This schema design provides a robust foundation for CapeControl's authentication system, supporting current needs while enabling future growth and compliance requirements.
