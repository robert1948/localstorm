# 🌩️ CapeControl V5

CapeControl is a modern AI-powered platform designed to give individuals and businesses access## 🚀 Architecture Overview

### Database Schema
- **Users Table**: Secure user management with role-based access
- **Tokens Table**: JWT session management with device tracking  
- **Developer Earnings**: Revenue tracking and commission management
- **Password Reset**: Secure password recovery workflow
- **Audit Logs**: Comprehensive security monitoring

See `/docs/database_schema.md` for detailed schema documentation.

### API Endpoints
- **Authentication**: Register, login, logout, refresh tokens
- **User Management**: Profile management, password changes
- **Developer Revenue**: Earnings tracking (developers only)
- **Security**: Role-based access control, audit logging

See `/docs/api_specification.md` for complete API documentation.

## 🌐 Deployment

### Production Deployment
Automatic deployment is triggered when code is pushed to the `main` branch via GitHub Actions.

**Infrastructure:**
- Docker images built and deployed to Heroku Container Registry
- Static frontend assets synced to AWS S3
- PostgreSQL database on Heroku Postgres
- Environment variables managed through Heroku Config Vars

**Live URLs:**
- **Production Site**: [https://cape-control.com](https://cape-control.com)
- **API Endpoint**: https://api.cape-control.com
- **Status Page**: https://api.cape-control.com/health

### Environment Configuration

**Required Environment Variables:**
```bash
# Security
SECRET_KEY=your-super-secure-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Database  
DATABASE_URL=postgresql://user:pass@localhost:5432/capecontrol

# Email (for password reset)
EMAIL_SMTP_HOST=smtp.gmail.com
EMAIL_USERNAME=your-email@gmail.com
EMAIL_PASSWORD=your-app-password

# URLs
FRONTEND_URL=https://cape-control.com
```

See `.env.example` files for complete configuration templates.

## 📚 Documentation

- **Database Schema**: `/docs/database_schema.md`
- **API Specification**: `/docs/api_specification.md` 
- **OpenAPI/Swagger**: `/docs/openapi.yaml`
- **Implementation Guide**: `/docs/implementation_guide.md`
- **Project Summary**: `/docs/project_summary.md`

## 🧹 Development Workflow

### Before Committing
```bash
# Run cleanup script
./scripts/pre-commit-cleanup.sh

# Check what will be committed
git status
git diff

# Ensure no sensitive files are included
git ls-files | grep -E '\.(env|key|pem)$' || echo "✅ No sensitive files found"
```

### Testing
```bash
# Run authentication system tests
cd backend
python test_auth_system.py

# Run frontend tests
cd client  
npm test
```e of **agentic services** — intelligent tools that automate tasks, boost productivity, and drive innovation.

## 🚀 Purpose

CapeControl is built to democratize access to AI by offering a dashboard where users can:

- **Register and log in securely** with JWT-based authentication
- **Browse a marketplace of AI agents** with role-based access
- **Activate services for specific goals** with personalized experiences
- **Track developer earnings** for AI agent creators
- **Use via subscription or pay-per-use** with integrated billing

The platform focuses on simplicity, scalability, and user empowerment, offering smart automation with zero coding required.

## 🔐 Authentication & Security

CapeControl features a **production-ready authentication system** with:

- **JWT Token Authentication** - Secure, stateless authentication
- **Role-Based Access Control** - Customer, Developer, and Admin roles
- **Password Security** - bcrypt hashing with salt
- **Developer Revenue Tracking** - Commission management and earnings analytics
- **Session Management** - Token refresh and revocation
- **Audit Logging** - Comprehensive security monitoring

### API Documentation
- **Interactive Docs**: http://localhost:8000/docs
- **OpenAPI Spec**: Available in `/docs/openapi.yaml`
- **Complete API Guide**: See `/docs/api_specification.md`

## 🛠 Tech Stack

- **Frontend:** React + Vite + Tailwind CSS
- **Backend:** FastAPI (Python) + SQLAlchemy
- **Authentication:** JWT + bcrypt + Role-based access
- **Database:** PostgreSQL (Production) / SQLite (Development)
- **DevOps:** Docker, GitHub Actions, Heroku Container Deploy
- **Hosting:** Heroku
- **Cloud Assets:** AWS S3
- **Editor:** VS Code (Codespaces Ready)

## ⚙️ Local Development

### 🔧 Prerequisites
- Python 3.11+ 
- Node.js 18+
- Git

### 🚀 Quick Start

1. **Clone the repository:**
```bash
git clone https://github.com/robert1948/localstorm.git
cd localstorm
```

2. **Set up environment variables:**
```bash
# Copy environment templates
cp .env.example .env
cp backend/.env.example backend/.env

# Update backend/.env with your configuration
```

3. **Backend Setup:**
```bash
cd backend
pip install -r requirements.txt

# Run database migrations (creates SQLite for development)
python migrate_auth.py

# Start the API server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

4. **Frontend Setup:**
```bash
cd client
npm install
npm run dev
```

5. **Docker (Full Stack):**
```bash
# Run the complete stack
docker-compose up --build
```

### 🌐 Access Points
- **Frontend**: http://localhost:5173 or http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

### 🧪 Testing the Authentication System

```bash
# Test user registration
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"Test123!","role":"developer"}'

# Test login
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"Test123!"}'

# Test protected endpoint (use token from login response)
curl -X GET http://localhost:8000/api/auth/me \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

4. **Docker (optional full stack):**

```bash
docker-compose up --build
```

5. **Visit the app locally:**

- Frontend: http://localhost:5173  
- Backend API: http://localhost:8000

## 🌐 Deployment

Automatic deployment is triggered when code is pushed to the `main` branch via GitHub Actions.  
Docker images are built and released to Heroku’s container registry.  
Static frontend assets are synced to an AWS S3 bucket.

Live site: [https://cape-control.com](https://cape-control.com)

## � Security Features

- **JWT Authentication**: Stateless, secure token-based auth
- **Password Hashing**: bcrypt with automatic salt generation  
- **Role-Based Access**: Customer, Developer, Admin permissions
- **Session Management**: Token refresh, revocation, device tracking
- **Security Monitoring**: Comprehensive audit logging
- **Input Validation**: Pydantic models with type safety
- **CORS Protection**: Configurable cross-origin policies
- **Rate Limiting**: Built-in abuse protection

## 🏆 Key Features

### For Customers
- ✅ Secure account registration and login
- ✅ Browse AI agent marketplace  
- ✅ Subscription and pay-per-use billing
- ✅ Personalized dashboard
- ✅ Usage analytics and history

### For Developers  
- ✅ AI agent publishing platform
- ✅ Revenue tracking and analytics
- ✅ Commission management (30% default)
- ✅ Payout history and reporting
- ✅ Developer-specific APIs

### For Administrators
- ✅ User management and analytics
- ✅ Platform oversight and monitoring
- ✅ Revenue reporting and insights
- ✅ Security audit logs

## �📄 License

MIT License © Robert

---

_Last updated: 2025-07-09 - Enhanced Authentication System v1.0_