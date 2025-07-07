# 🌩️ CapeControl V5

CapeControl is a modern AI-powered platform designed to give individuals and businesses access to a curated suite of **agentic services** — intelligent tools that automate tasks, boost productivity, and drive innovation.

## 🚀 Purpose

CapeControl is built to democratize access to AI by offering a dashboard where users can:

- Register and log in securely
- Browse a marketplace of AI agents
- Activate services for specific goals
- Use via subscription or pay-per-use

The platform focuses on simplicity, scalability, and user empowerment, offering smart automation with zero coding required.

## 🛠 Tech Stack

- **Frontend:** React + Vite + Tailwind CSS
- **Backend:** FastAPI (Python)
- **Database:** PostgreSQL
- **DevOps:** Docker, GitHub Actions, Heroku Container Deploy
- **Hosting:** Heroku
- **Cloud Assets:** AWS S3
- **Editor:** VS Code (Codespaces Ready)

## ⚙️ Local Development

1. **Clone the repo:**

```bash
git clone https://github.com/robert1948/localstorm.git
cd localstorm
```

2. **Frontend Setup:**

```bash
cd client
npm install
npm run dev
```

3. **Backend Setup:**

```bash
cd backend
pip install -r requirements.txt
uvicorn src.main:app --reload
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

## 📄 License

MIT License © Robert

---

_Last updated: 2025-07-03_