# 🚀 CapeControl — Phase 2 Checklist: Production & AI Agents

This phase focuses on going live, hardening infrastructure, and beginning intelligent agent integration.

---

## 🌐 Production Deployment

### ✅ Environment Setup
- [ ] Create `.env.production` file for Heroku/Render
- [ ] Set `DATABASE_URL`, `SECRET_KEY`, `CORS_ORIGIN`, etc. in platform config
- [ ] Enable HTTPS enforcement

### 🚢 Deployment Targets
- [ ] Deploy FastAPI backend to Heroku or Render
- [ ] Attach Heroku Postgres or Render Database
- [ ] Deploy Vite frontend (e.g., Netlify or Render static site)
- [ ] Configure custom domain (optional)
- [ ] Point frontend to live backend URL

### 🔁 Automation & CI/CD
- [ ] Add GitHub Actions for backend test/lint
- [ ] Add deployment trigger on main branch
- [ ] Add lint checks for frontend code

---

## 🔒 Security & Stability

- [ ] Use strong generated `SECRET_KEY` in production
- [ ] Restrict CORS to production frontend
- [ ] Enable database backups
- [ ] Enforce token expiration & refresh
- [ ] Add rate limiting middleware

---

## 🧠 AI Agent Features — Phase 1

### Agent Vision
“CapeAI” should assist users with onboarding, checklists, and intelligent suggestions.

### ✅ Core Capabilities
- [ ] Display welcome message + contextual guide
- [ ] Auto-suggest next action based on user role/status
- [ ] Respond to onboarding queries via UI widget

### 🧠 Backend Agent Logic
- [ ] Add `/agent/prompt` route
- [ ] Accept chat input & user context
- [ ] Respond with intelligent suggestions (using OpenAI API or local model)

### 💬 Frontend Integration
- [ ] Create persistent AI widget or sidebar
- [ ] Hook to `/agent/prompt` route
- [ ] Display streamed or chunked responses (optional)

---

## 🧪 Monitoring & Feedback

- [ ] Add logging of agent prompts and responses
- [ ] Store user actions to refine onboarding paths
- [ ] Add basic analytics dashboard

---

## 📦 Optional Enhancements

- [ ] Add Stripe for agentic subscriptions
- [ ] Enable in-app messaging with agent memory
- [ ] Multi-tenant project-based AI assistants
- [ ] Offline fallback prompts for mobile users

---

## 🚀 Go Live!

- [ ] Final smoke test
- [ ] Send launch announcement
- [ ] Share on LinkedIn + product boards