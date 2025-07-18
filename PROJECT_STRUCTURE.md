# 🏗️ CapeControl Project Structure

## 📁 Root Directory
```
/workspaces/localstorm-main/
├── 🚀 backend/           # FastAPI backend application
├── 🎨 client/            # React frontend application  
├── ☁️ cloudflare-workers/ # Edge workers for CDN
├── 📚 docs/              # Organized documentation
├── 🔧 scripts/           # Utility and test scripts
├── 🐳 .devcontainer/     # VS Code dev container config
├── 📄 .env               # Development environment variables
└── 📄 config files       # Environment and deployment configs
```

## 🚀 Backend (`/backend/`)
```
backend/
├── app/                  # Main FastAPI application
│   ├── main.py          # FastAPI app entry point
│   ├── config.py        # Application configuration
│   ├── models.py        # Database models
│   ├── schemas.py       # Pydantic schemas
│   ├── auth.py          # Authentication logic
│   ├── database.py      # Database connection
│   ├── routes/          # API route handlers
│   └── static/          # Frontend build files
├── scripts/             # Migration and setup scripts
├── Dockerfile           # Backend container config
└── auth_api_standalone.py # Standalone auth server
```

## 🎨 Frontend (`/client/`)
```
client/
├── src/                 # React source code
│   ├── components/      # Reusable UI components
│   │   ├── 🤖 CapeAIChat.jsx           # Full-featured chat interface
│   │   ├── 🤖 CapeAIFloatingButton.jsx # Draggable floating chat button
│   │   ├── 🤖 CapeAISystem.jsx         # Integration component
│   │   ├── onboarding/                 # Onboarding components
│   │   │   ├── 🤖 OnboardingChecklist.jsx # Interactive checklist
│   │   │   └── 🤖 OnboardingFlow.jsx      # Automated flow manager
│   │   ├── Navbar.jsx                  # Navigation component
│   │   └── ProtectedRoute.jsx          # Route protection
│   ├── context/         # React Context providers
│   │   └── 🤖 CapeAIContext.jsx        # Enhanced CapeAI state management
│   ├── hooks/           # Custom React hooks
│   │   ├── 🤖 useCapeAI.jsx            # CapeAI context hook
│   │   ├── 🤖 useOnboarding.jsx        # Smart onboarding management
│   │   └── useAuth.jsx                 # Authentication hook
│   ├── pages/           # Page components
│   │   ├── Dashboard.jsx               # Enhanced with onboarding
│   │   ├── Landing.jsx                 # Landing page
│   │   └── [other pages]               # Login, Register, etc.
│   ├── utils/           # Utility functions
│   └── styles/          # CSS and styling
├── public/              # Static assets
├── dist/                # Build output
├── package.json         # Dependencies and scripts
├── vite.config.js       # Vite build configuration
└── tailwind.config.js   # Tailwind CSS config
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
