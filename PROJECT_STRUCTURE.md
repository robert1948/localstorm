# 🏗️ LocalStorm Project Architecture

**Updated:** July 24, 2025 | **Status:** Production-Ready with AI Intelligence

## 📁 **Root Directory Structure**
```
/workspaces/localstorm/
├── 🚀 backend/              # FastAPI backend (Python 3.11) with AI Services
├── 🎨 client/               # React 19.1.0 frontend (Mobile-First + AI-Enhanced)
├── ☁️ cloudflare-workers/   # Edge workers with AI routing optimization
├── 📚 docs/                 # Comprehensive documentation + AI guides
├── 🔧 scripts/              # Deployment & utility scripts (S3 + AI deployments)
├── 🐳 .devcontainer/        # VS Code dev container with AI development tools
├── 📄 .env                  # Production environment with AI API keys
├── 🤖 CapeAI Implementation Files:
│   ├── CAPEAI_DEVELOPMENT_PLAN.md      # Comprehensive AI roadmap
│   ├── CAPEAI_INTEGRATION_GUIDE.md     # Step-by-step implementation
│   ├── CAPEAI_IMPLEMENTATION_CHECKLIST.md # Production deployment guide
│   └── PRODUCTION_APP_ROUTE_FIX.md     # Cloudflare routing solution
├── 🛠️ apply_security_fixes.sh # Security hardening with AI monitoring
├── 📋 *_AUDIT.md            # Security and deployment documentation
├── 📱 MOBILE_TAILWIND_IMPLEMENTATION.md # Mobile-first design documentation
└── 🔧 configuration files   # Docker, Heroku, CI/CD with AI service configs
```

## 🚀 **Backend Architecture** (`/backend/`)
```
backend/
├── app/                     # FastAPI application core with AI services
│   ├── main.py             # Application entry + CORS + AI route integration
│   ├── config/             # Configuration management
│   │   └── cape_ai_config.py # AI service configurations and feature flags
│   ├── database.py         # PostgreSQL connection (AWS RDS) + AI analytics tables
│   ├── dependencies.py     # Dependency injection + AI service dependencies
│   ├── models.py           # SQLAlchemy models + AI conversation schemas
│   ├── schemas.py          # Pydantic validation + AI request/response models
│   ├── auth.py             # JWT authentication with AI security features
│   ├── routes/             # API endpoint modules
│   │   ├── auth.py         # Legacy auth endpoints
│   │   ├── auth_v2.py      # Enhanced auth with v2 features
│   │   ├── auth_enhanced.py # Production auth system
│   │   └── 🤖 cape_ai.py   # AI assistant endpoints (OpenAI + Redis integration)
│   ├── services/           # Business logic services
│   │   └── ai_service.py   # CapeAI intelligence engine (context-aware responses)
│   └── static/             # Frontend build integration (AI-enhanced mobile UI)
├── tests/                  # Comprehensive test suite + AI endpoint tests
│   └── test_auth.py        # Authentication + AI security tests
├── migrations/             # Database migration scripts + AI schema updates
├── Dockerfile              # Production container with AI dependencies
└── standalone services     # Development utilities + AI testing tools
```

## 🎨 **Frontend Architecture** (`/client/`)
```
client/
├── src/                    # React 19.1.0 source (AI-Enhanced + Mobile-First)
│   ├── components/         # Reusable UI components (AI-Integrated + Touch-Optimized)
│   │   ├── 🤖 AI System Components (Production-Ready):
│   │   │   ├── CapeAIChat.jsx           # Basic chat interface (legacy)
│   │   │   ├── CapeAIChatEnhanced.jsx   # Advanced AI chat with OpenAI integration
│   │   │   ├── CapeAISystem.jsx         # AI system orchestrator
│   │   │   └── OnboardingChecklist.jsx  # AI-guided onboarding
│   │   ├── 📋 Onboarding Components:
│   │   │   ├── OnboardingChecklist.jsx  # Interactive progress tracker
│   │   │   └── OnboardingFlow.jsx       # Automated flow manager
│   │   ├── 🧭 Navigation & Layout:
│   │   │   ├── Navbar.jsx               # Main navigation (S3 logo + mobile hamburger)
│   │   │   ├── Hero.jsx                 # Landing hero (S3 images + responsive)
│   │   │   └── ProtectedRoute.jsx       # Route authentication
│   │   └── 🎯 Feature Components        # Forms, modals, etc. (Mobile-optimized)
│   ├── context/            # React Context providers  
│   │   ├── 🤖 CapeAIContext.jsx        # AI assistant state management
│   │   ├── 🤖 CapeAIContextSafe.jsx    # Safe AI context with fallbacks
│   │   └── AuthContext.jsx             # Authentication state
│   ├── hooks/              # Custom React hooks (Hook Rules Compliant)
│   │   ├── 🤖 useCapeAI.jsx            # Basic CapeAI integration hook
│   │   ├── 🤖 useCapeAIEnhanced.jsx    # Advanced AI hook with OpenAI API
│   │   ├── 🤖 useOnboarding.jsx        # Onboarding flow management
│   │   └── useAuth.jsx                 # Authentication utilities
│   ├── pages/              # Route-based page components (Mobile-First)
│   │   ├── Landing.jsx                 # Public landing (Touch-optimized)
│   │   ├── Dashboard.jsx               # User dashboard with AI integration
│   │   ├── auth/                       # Authentication pages (Mobile forms)
│   │   └── platform/                   # Platform pages (AI-enhanced)
│   ├── api/                # API integration layer + AI endpoints
│   ├── utils/              # Utility functions + AI helpers
│   └── styles/             # CSS styling system (Mobile-First Tailwind)
│       ├── globals.css     # Global styles (7.11kB optimized)
│       └── components.css  # Component-specific styles
├── public/                 # Static assets
│   ├── static/             # Images (synced to S3)
│   │   ├── LogoC.png       # Color logo (1.4MB) - S3 hosted
│   │   ├── LogoW.png       # White logo (326KB) - S3 hosted  
│   │   ├── landing01.png   # Hero image (503KB) - S3 hosted
│   │   ├── capecontrol-logo.png # Brand logo (2.7KB) - S3 hosted
│   │   └── favicon files   # PWA icons - All S3 hosted
│   ├── manifest.json       # PWA manifest (S3 URLs)
│   └── site.webmanifest    # Web manifest (S3 URLs)
├── dist/                   # Vite build output
├── package.json            # Dependencies (React 19.1.0, Vite 6.3.5, Tailwind)
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
├── 📦 Static Assets       # AWS S3 (lightning-s3.s3.us-east-1.amazonaws.com)
│   ├── 🖼️ Images          # All PNG/ICO files (14 total, 2.8MB)
│   ├── 📱 PWA Icons       # Progressive Web App manifest icons
│   └── 🎨 Brand Assets    # Logos, landing images, favicons
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
