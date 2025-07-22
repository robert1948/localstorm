# 🏗️ LocalStorm Project Architecture

**Updated:** July 20, 2025 | **Status:** Production-Ready & Localhost Operational

## 📁 **Root Directory Structure**
```
/workspaces/localstorm/
├── 🚀 backend/              # FastAPI backend (Python 3.11)
├── 🎨 client/               # React frontend (Vite + TailwindCSS)
├── ☁️ cloudflare-workers/   # Edge workers for CDN optimization
├── 📚 docs/                 # Comprehensive documentation
├── 🔧 scripts/              # Deployment & utility scripts
├── 🐳 .devcontainer/        # VS Code dev container config
├── 📄 .env                  # Production-connected environment
├── 🛠️ apply_security_fixes.sh # Security hardening script
├── 📋 *_AUDIT.md            # Security and deployment documentation
└── 🔧 configuration files   # Docker, Heroku, CI/CD configs
```

## 🚀 **Backend Architecture** (`/backend/`)
```
backend/
├── app/                     # FastAPI application core
│   ├── main.py             # Application entry point + CORS
│   ├── config.py           # Configuration management
│   ├── database.py         # PostgreSQL connection (AWS RDS)
│   ├── dependencies.py     # Dependency injection
│   ├── models.py           # SQLAlchemy database models
│   ├── schemas.py          # Pydantic validation schemas
│   ├── auth.py             # JWT authentication logic
│   ├── routes/             # API endpoint modules
│   │   ├── auth.py         # Legacy auth endpoints
│   │   ├── auth_v2.py      # Enhanced auth with v2 features
│   │   └── auth_enhanced.py # Production auth system
│   └── static/             # Frontend build integration
├── tests/                  # Comprehensive test suite
│   └── test_auth.py        # Authentication endpoint tests
├── migrations/             # Database migration scripts
├── Dockerfile              # Production container config
└── standalone services     # Development utilities
```

## 🎨 **Frontend Architecture** (`/client/`)
```
client/
├── src/                    # React 18 source code
│   ├── components/         # Reusable UI components
│   │   ├── 🤖 CapeAI System Components:
│   │   │   ├── CapeAIChat.jsx           # Advanced chat interface
│   │   │   ├── CapeAIFloatingButton.jsx # Draggable floating button
│   │   │   └── CapeAISystem.jsx         # Core integration hub
│   │   ├── 📋 Onboarding Components:
│   │   │   ├── OnboardingChecklist.jsx  # Interactive progress tracker
│   │   │   └── OnboardingFlow.jsx       # Automated flow manager
│   │   ├── 🧭 Navigation & Layout:
│   │   │   ├── Navbar.jsx               # Main navigation (S3 logo)
│   │   │   ├── Hero.jsx                 # Landing hero (S3 images)
│   │   │   └── ProtectedRoute.jsx       # Route authentication
│   │   └── 🎯 Feature Components        # Forms, modals, etc.
│   ├── context/            # React Context providers
│   │   ├── 🤖 CapeAIContext.jsx        # AI assistant state management
│   │   └── AuthContext.jsx             # Authentication state
│   ├── hooks/              # Custom React hooks
│   │   ├── 🤖 useCapeAI.jsx            # CapeAI integration hook
│   │   ├── 🤖 useOnboarding.jsx        # Onboarding flow management
│   │   └── useAuth.jsx                 # Authentication utilities
│   ├── pages/              # Route-based page components
│   │   ├── Landing.jsx                 # Public landing page
│   │   ├── Dashboard.jsx               # User dashboard with CapeAI
│   │   ├── auth/                       # Authentication pages
│   │   └── platform/                   # Platform-specific pages
│   ├── api/                # API integration layer
│   ├── utils/              # Utility functions
│   └── styles/             # CSS and styling system
├── public/                 # Static assets
│   └── static/             # Images synced to S3
├── dist/                   # Vite build output
├── package.json            # Dependencies (React 18, Vite, Tailwind)
├── vite.config.js          # Vite configuration + cache busting
└── tailwind.config.js      # Tailwind CSS configuration
```

## 🔐 **Security & Configuration**
```
Security Implementation:
├── 🔑 JWT Authentication    # Stateless token-based auth
├── 🛡️ Production Security   # Secure SECRET_KEY, environment isolation
├── 🗄️ Database Security     # AWS RDS encrypted connections
├── 🌐 CORS Protection      # Configurable cross-origin policies
├── 📝 Input Validation     # Pydantic models with type safety
└── 🔒 Environment Variables # Production secrets management
```

## ☁️ **Infrastructure & Assets**
```
Production Infrastructure:
├── 🏗️ Deployment Platform  # Heroku (Docker containers)
├── 🗄️ Database            # AWS RDS PostgreSQL (production-grade)
├── 📦 Static Assets       # AWS S3 (lightning-s3 bucket)
├── 🔄 CI/CD               # GitHub Actions (automated testing)
└── 🌐 CDN                 # S3 + CloudFront for global delivery
```

## 📚 Documentation (`/docs/`)
```
docs/
├── archive/             # Historical documentation
├── development/         # Development guides and notes
├── checklists/          # Project checklists and milestones
└── api/                 # API documentation
```

## 🔧 Scripts (`/scripts/`)
```
scripts/
├── setup/               # Database and environment setup
├── tests/               # Test scripts and utilities
└── deployment/          # Deployment scripts
```

## 🌍 Environment Files
- `.env` - Development environment variables (✅ configured)
- `.env.example` - Environment template
- `.env.email.example` - Email configuration template

## 🐳 Development Container
- `.devcontainer/devcontainer.json` - VS Code dev container configuration
- `.devcontainer/Dockerfile` - Container build definition
- **Features**: Automatic npm/pip install, environment setup, port forwarding

## 🚀 Getting Started

### Development Server (Recommended - Dev Container)
```bash
# Open in VS Code and reopen in container
code .
# Container automatically installs dependencies

# Start both services
bash ./scripts/start_localstorm.sh

# OR use Makefile
make dev
```

### Manual Development Server
```bash
# Backend (FastAPI) - from project root
cd backend && python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Frontend (React + Vite) - from project root, new terminal
cd client && npm run dev -- --port 3000 --host 0.0.0.0
```

### Access URLs
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000  
- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/api/health
- **🤖 CapeAI Assistant**: Available on all frontend pages via floating chat button

### 🤖 CapeAI System Overview
The CapeAI onboarding assistant system includes:

1. **CapeAIContext.jsx**: Enhanced React context with onboarding state management
2. **CapeAISystem.jsx**: Main integration component connecting all CapeAI features
3. **CapeAIFloatingButton.jsx**: Draggable floating chat interface with smart positioning
4. **OnboardingFlow.jsx**: Automated onboarding guidance system
5. **OnboardingChecklist.jsx**: Interactive checklist with CapeAI integration
6. **useOnboarding.jsx**: Smart hook for managing onboarding state and progress
7. **useCapeAI.jsx**: Context hook for accessing CapeAI functionality

### Production Build
```bash
# Build frontend
cd client && npm run build

# Run full stack
cd backend && python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## 🐳 Docker & Deployment
- `Dockerfile` - Backend container
- `docker-compose.yml` - Multi-service orchestration
- `Procfile` - Heroku deployment
- `heroku.yml` - Heroku container deployment
- `app.json` - Heroku app configuration

## 🎯 **Project Status**

- **Production URL**: https://www.cape-control.com
- **Development**: VS Code Dev Container + Docker  
- **Status**: ✅ Live and fully operational with CapeAI onboarding system
- **Latest Features**: 🤖 CapeAI intelligent onboarding assistant (July 18, 2025)

---
*Last updated: July 18, 2025 - Added comprehensive CapeAI onboarding assistant system*
