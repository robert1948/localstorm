# CapeControl Authentication API Specification
## Complete REST API Documentation

### Overview
This document provides the complete API specification for CapeControl's secure authentication system. All endpoints follow REST conventions and return JSON responses.

**Base URL**: `https://api.capecontrol.com`  
**API Version**: `v1`  
**Authentication**: JWT Bearer tokens

---

## Table of Contents
1. [Authentication Endpoints](#authentication-endpoints)
2. [User Management](#user-management)
3. [Developer Revenue](#developer-revenue)
4. [Data Models](#data-models)
5. [Error Handling](#error-handling)
6. [Security](#security)

---

## Authentication Endpoints

### POST /api/auth/register
Register a new user account.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "SecurePassword123!",
  "first_name": "John",
  "last_name": "Doe",
  "role": "customer",
  "phone": "+1-555-0123",
  "website": "https://example.com",
  "company": "Example Corp",
  "experience": "intermediate"
}
```

**Response (201 Created):**
```json
{
  "success": true,
  "message": "User registered successfully",
  "data": {
    "user": {
      "id": 1,
      "email": "user@example.com",
      "first_name": "John",
      "last_name": "Doe",
      "role": "customer",
      "is_active": true,
      "is_verified": false,
      "created_at": "2025-01-08T10:30:00Z"
    },
    "tokens": {
      "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
      "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
      "token_type": "bearer",
      "expires_in": 3600
    }
  }
}
```

**Validation Rules:**
- Email must be valid and unique
- Password minimum 8 characters, must include uppercase, lowercase, number
- Role must be: `customer`, `developer`, or `admin`
- Experience must be: `beginner`, `intermediate`, `advanced`, or `expert`

---

### POST /api/auth/login
Authenticate user and receive JWT tokens.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "SecurePassword123!"
}
```

**Response (200 OK):**
```json
{
  "success": true,
  "message": "Login successful",
  "data": {
    "user": {
      "id": 1,
      "email": "user@example.com",
      "first_name": "John",
      "last_name": "Doe",
      "role": "customer",
      "last_login_at": "2025-01-08T10:30:00Z"
    },
    "tokens": {
      "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
      "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
      "token_type": "bearer",
      "expires_in": 3600
    }
  }
}
```

**Error Response (401 Unauthorized):**
```json
{
  "success": false,
  "message": "Invalid credentials",
  "error_code": "INVALID_CREDENTIALS"
}
```

---

### POST /api/auth/logout
Invalidate current JWT tokens.

**Headers:**
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Response (200 OK):**
```json
{
  "success": true,
  "message": "Logout successful"
}
```

---

### POST /api/auth/refresh
Refresh access token using refresh token.

**Request Body:**
```json
{
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Response (200 OK):**
```json
{
  "success": true,
  "message": "Token refreshed successfully",
  "data": {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "token_type": "bearer",
    "expires_in": 3600
  }
}
```

---

### POST /api/auth/reset-password
Request password reset email.

**Request Body:**
```json
{
  "email": "user@example.com"
}
```

**Response (200 OK):**
```json
{
  "success": true,
  "message": "Password reset email sent"
}
```

**Note**: Always returns success to prevent email enumeration attacks.

---

### POST /api/auth/reset-password/confirm
Confirm password reset with token.

**Request Body:**
```json
{
  "token": "reset_token_from_email",
  "new_password": "NewSecurePassword123!"
}
```

**Response (200 OK):**
```json
{
  "success": true,
  "message": "Password reset successfully"
}
```

---

## User Management

### GET /api/auth/me
Get current user profile.

**Headers:**
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "id": 1,
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "role": "customer",
    "phone": "+1-555-0123",
    "website": "https://example.com",
    "company": "Example Corp",
    "experience": "intermediate",
    "is_active": true,
    "is_verified": false,
    "created_at": "2025-01-08T10:30:00Z",
    "last_login_at": "2025-01-08T10:30:00Z"
  }
}
```

---

### PUT /api/auth/me
Update current user profile.

**Headers:**
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Request Body:**
```json
{
  "first_name": "John",
  "last_name": "Smith",
  "phone": "+1-555-0124",
  "website": "https://newsite.com",
  "company": "New Company",
  "experience": "advanced"
}
```

**Response (200 OK):**
```json
{
  "success": true,
  "message": "Profile updated successfully",
  "data": {
    "id": 1,
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Smith",
    "phone": "+1-555-0124",
    "website": "https://newsite.com",
    "company": "New Company",
    "experience": "advanced",
    "updated_at": "2025-01-08T11:00:00Z"
  }
}
```

---

### POST /api/auth/change-password
Change user password.

**Headers:**
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Request Body:**
```json
{
  "current_password": "SecurePassword123!",
  "new_password": "NewSecurePassword456!"
}
```

**Response (200 OK):**
```json
{
  "success": true,
  "message": "Password changed successfully"
}
```

---

## Developer Revenue

### GET /api/auth/developer/earnings
Get developer earnings summary (Developer role required).

**Headers:**
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Query Parameters:**
- `page` (optional): Page number for pagination (default: 1)
- `limit` (optional): Items per page (default: 10, max: 100)
- `agent_id` (optional): Filter by specific agent ID

**Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "summary": {
      "total_revenue_share": 1250.75,
      "total_paid_out": 800.00,
      "pending_payout": 450.75,
      "active_agents": 3,
      "currency": "USD"
    },
    "earnings": [
      {
        "id": 1,
        "agent_id": "agent_001",
        "agent_name": "Marketing AI Assistant",
        "revenue_share": 750.50,
        "total_sales": 2501.67,
        "commission_rate": 0.3000,
        "last_payout_amount": 500.00,
        "last_payout_at": "2025-01-01T00:00:00Z",
        "total_paid_out": 500.00,
        "is_active": true,
        "created_at": "2024-12-01T00:00:00Z"
      },
      {
        "id": 2,
        "agent_id": "agent_002",
        "agent_name": "Customer Support Bot",
        "revenue_share": 500.25,
        "total_sales": 1667.50,
        "commission_rate": 0.3000,
        "last_payout_amount": 300.00,
        "last_payout_at": "2025-01-01T00:00:00Z",
        "total_paid_out": 300.00,
        "is_active": true,
        "created_at": "2024-11-15T00:00:00Z"
      }
    ],
    "pagination": {
      "page": 1,
      "limit": 10,
      "total": 2,
      "total_pages": 1
    }
  }
}
```

---

## Data Models

### User Model
```json
{
  "id": "integer",
  "email": "string (email format)",
  "first_name": "string (optional)",
  "last_name": "string (optional)",
  "role": "enum (customer|developer|admin)",
  "phone": "string (optional)",
  "website": "string (URL, optional)",
  "company": "string (optional)",
  "experience": "enum (beginner|intermediate|advanced|expert, optional)",
  "is_active": "boolean",
  "is_verified": "boolean",
  "created_at": "string (ISO 8601)",
  "updated_at": "string (ISO 8601, optional)",
  "last_login_at": "string (ISO 8601, optional)"
}
```

### Token Model
```json
{
  "access_token": "string (JWT)",
  "refresh_token": "string (JWT, optional)",
  "token_type": "string (always 'bearer')",
  "expires_in": "integer (seconds)"
}
```

### Developer Earning Model
```json
{
  "id": "integer",
  "agent_id": "string",
  "agent_name": "string (optional)",
  "revenue_share": "number (decimal)",
  "total_sales": "number (decimal)",
  "commission_rate": "number (decimal, 0-1)",
  "last_payout_amount": "number (decimal)",
  "last_payout_at": "string (ISO 8601, optional)",
  "total_paid_out": "number (decimal)",
  "is_active": "boolean",
  "currency": "string (3-char code)",
  "created_at": "string (ISO 8601)",
  "updated_at": "string (ISO 8601, optional)"
}
```

---

## Error Handling

### Standard Error Response
```json
{
  "success": false,
  "message": "Human-readable error message",
  "error_code": "MACHINE_READABLE_CODE",
  "details": {
    "field": "Additional error details"
  }
}
```

### HTTP Status Codes
- `200 OK` - Request successful
- `201 Created` - Resource created successfully
- `400 Bad Request` - Invalid request data
- `401 Unauthorized` - Authentication required or failed
- `403 Forbidden` - Insufficient permissions
- `404 Not Found` - Resource not found
- `409 Conflict` - Resource already exists
- `422 Unprocessable Entity` - Validation errors
- `500 Internal Server Error` - Server error

### Common Error Codes
- `INVALID_CREDENTIALS` - Login failed
- `EMAIL_ALREADY_EXISTS` - Registration with existing email
- `INVALID_TOKEN` - JWT token is invalid or expired
- `INSUFFICIENT_PERMISSIONS` - User lacks required role
- `VALIDATION_ERROR` - Request validation failed
- `PASSWORD_TOO_WEAK` - Password doesn't meet requirements
- `ACCOUNT_DEACTIVATED` - User account is disabled

---

## Security

### Authentication
- **JWT Tokens**: HS256 signed tokens with configurable expiration
- **Refresh Tokens**: Long-lived tokens for access token renewal
- **Token Revocation**: Ability to invalidate tokens server-side

### Password Security
- **Hashing**: bcrypt with automatic salt generation
- **Strength Requirements**: Minimum 8 characters, mixed case, numbers
- **Reset Flow**: Secure token-based password reset

### Access Control
- **Role-Based**: Customer, Developer, Admin roles
- **Endpoint Protection**: JWT required for protected endpoints
- **Permission Checks**: Role validation for sensitive operations

### Rate Limiting
- **Login Attempts**: Max 5 failed attempts per 15 minutes
- **Registration**: Max 3 registrations per IP per hour
- **Password Reset**: Max 3 requests per email per hour

### Audit Logging
- All authentication events logged
- IP address and user agent tracking
- Failed login attempt monitoring
- Security event alerting

---

## Postman Collection

### Authentication Flow Example

1. **Register New User**
   ```
   POST /api/auth/register
   Content-Type: application/json
   
   {
     "email": "developer@example.com",
     "password": "DevPassword123!",
     "role": "developer",
     "first_name": "Jane",
     "last_name": "Developer"
   }
   ```

2. **Login**
   ```
   POST /api/auth/login
   Content-Type: application/json
   
   {
     "email": "developer@example.com",
     "password": "DevPassword123!"
   }
   ```

3. **Access Protected Resource**
   ```
   GET /api/auth/me
   Authorization: Bearer {{access_token}}
   ```

4. **Refresh Token**
   ```
   POST /api/auth/refresh
   Content-Type: application/json
   
   {
     "refresh_token": "{{refresh_token}}"
   }
   ```

5. **Get Developer Earnings**
   ```
   GET /api/auth/developer/earnings
   Authorization: Bearer {{access_token}}
   ```

### Environment Variables
```json
{
  "base_url": "https://api.capecontrol.com",
  "access_token": "{{access_token_from_login}}",
  "refresh_token": "{{refresh_token_from_login}}"
}
```

This API specification provides a complete, production-ready authentication system for CapeControl with proper security, developer revenue tracking, and comprehensive error handling.
