# 🏗️ CapeControl Project Structure

## 📁 Root Directory
```
/workspaces/localstorm/
├── 🚀 backend/           # FastAPI backend application
├── 🎨 client/            # React frontend application  
├── ☁️ cloudflare-workers/ # Edge workers for CDN
├── 📚 docs/              # Organized documentation
├── 🔧 scripts/           # Utility and test scripts
├── 🐳 .devcontainer/     # VS Code dev container config
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
- `.env` - Development environment variables
- `.env.example` - Environment template
- `.env.production` - Production configuration
- `.env.email.example` - Email configuration template

## 🐳 Docker & Deployment
- `Dockerfile` - Backend container
- `docker-compose.yml` - Multi-service orchestration
- `Procfile` - Heroku deployment
- `heroku.yml` - Heroku container deployment
- `app.json` - Heroku app configuration

## 🚀 Getting Started

### Development Server
```bash
# Backend (FastAPI)
cd backend && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Frontend (React + Vite)  
cd client && npm run dev
```

### Production Build
```bash
# Build frontend
cd client && npm run build

# Run full stack
uvicorn backend.app.main:app --host 0.0.0.0 --port 8000
```

---
*Last updated: July 14, 2025*
