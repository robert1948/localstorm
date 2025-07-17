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
│   ├── pages/           # Page components
│   ├── hooks/           # Custom React hooks
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

---
*Last updated: July 17, 2025*
