
---

## 🧪 Live App

🌐 [https://tailstorm.herokuapp.com](https://tailstorm.herokuapp.com)

📄 [API Docs](https://tailstorm.herokuapp.com/docs)

---

## 🤝 Contributing

This repo is structured for collaborative scaling. To join, fork this repo, clone locally, and create a feature branch. PRs are welcome.

---

© 2025 CapeControl · Built with ❤️ in Cape Town
Checklist# ✅ CapeControl Development Checklist — V2

This version expands direction for production readiness, clean coding practices, and deployment.

---

## 🔧 Backend (FastAPI)

### ✅ Auth & Routes
- [x] Register & login with JWT
- [x] `/me` protected route
- [x] `/logout` (JWT deletion client-side)
- [ ] `/refresh` token support (optional)
- [x] Move route logic into `app/routes/`
- [x] Move dependencies into `dependencies.py`

### ✅ Configuration
- [x] Use `dotenv` and `.env`
- [x] Create `app/config.py` with `Settings` class
- [x] Access all settings from `settings.` import
- [x] Environment override support (`CORS_ORIGIN=*`)

### ✅ Database
- [x] PostgreSQL container in `docker-compose.yml`
- [x] Use `SessionLocal` via `get_db()` dependency
- [ ] Add Alembic for migrations
- [ ] Add seed script for test users
- [ ] Add SQLAlchemy relationship support

---

## 🧠 Frontend (React + Vite + Tailwind)

### ✅ Auth Flow
- [x] Login / Register / Logout
- [x] AuthContext for token & user state
- [x] ProtectedRoute component
- [x] Redirect on login success
- [x] Show email in navbar
- [ ] Refresh token on page reload (optional)

### ✅ UI / UX
- [x] Responsive Navbar with auth-aware links
- [x] Form validation + error display
- [x] Code-splitting via lazy loading
- [x] Loading spinner on route guards
- [ ] Add toast notifications for success/errors

### ✅ Code Style
- [x] ESLint + Prettier configured
- [x] Component and layout separation
- [ ] Convert core files to `.tsx` or add PropTypes

---

## 📦 DevOps & Deployment

### ✅ Local Dev
- [x] Dockerized backend + PostgreSQL
- [x] React runs via Vite on port 5173
- [x] Local `.env` for secrets
- [x] Swagger UI on `/docs`

### 🛰️ Deployment (Heroku/Render)
- [ ] Set environment variables
- [ ] Attach Heroku Postgres
- [ ] `Procfile` for FastAPI
- [ ] Enable automatic GitHub deploys
- [ ] Set CORS/FRONTEND_ORIGIN envs

---

## 🧪 Testing & CI

- [ ] Add `tests/` folder with `pytest`
- [ ] Add `prestart.sh` script for DB checks
- [ ] GitHub Actions workflow for CI:
    - Install
    - Lint
    - Test backend
- [ ] Optionally test React with Vitest or Jest

---

## 🔮 Future (Optional Ideas)

- [ ] Add admin role + access control
- [ ] Add multi-user organization support
- [ ] Rate limiting with FastAPI middleware
- [ ] Connect Stripe or PayPal
- [ ] AI onboarding assistant# Test deploy
# Test deploy
