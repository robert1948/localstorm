Here’s the updated and cleaned-up version of `Checklist.md` based on your latest project state and priorities:

---

# 📋 CapeControl Development Checklist

## ✅ Backend

* [x] Setup FastAPI app with CORS middleware
* [x] Create `/register` and `/login` routes
* [x] Add password hashing and token creation
* [x] Implement `/me` protected route
* [x] Move all backend code into `backend/app/` for clarity and maintainability
* [x] Organize route files under `backend/app/routes/` and include routers modularly in `main.py`
* [x] Ensure all backend imports use `from app ...` instead of `from backend ...`
* [ ] Use environment variables for sensitive data (e.g., database URLs) in backend
* [ ] Add a `get_db` dependency for database sessions in FastAPI
* [ ] Add role-based access control
* [ ] Add error logging to all routes
* [ ] Add docstrings and comments to all models, schemas, and complex logic
* [x] Use `from_attributes = True` in Pydantic schema `Config` for ORM mode
* [x] Move utility scripts to the `scripts/` directory
* [x] Ensure Docker and Compose files are at the project root and updated for new structure

## ✅ Frontend (React + Tailwind)

* [x] Setup Vite + Tailwind project
* [x] Create `Login` and `Register` forms
* [x] Login form deployed on live Heroku instance
* [x] Hook login form to backend
* [x] Store token in localStorage
* [x] Create Dashboard with `/me` fetch
* [ ] Centralize error handling in hooks and API utilities
* [ ] Refactor long functions into smaller, modular pieces
* [ ] Extract reusable logic (like data fetching) into custom hooks with JSDoc comments
* [ ] Use functional components and hooks in React code
* [ ] Use `useMemo` and `useCallback` for performance optimization in React
* [ ] Use PropTypes or TypeScript for type checking in React components
* [ ] Add and configure ESLint with a custom config to enforce:
  \- camelCase for variables and functions
  \- single quotes for string literals
  \- 2-space indentation
* [ ] Add Prettier for consistent code formatting
* [ ] Add an `ignores` property in `eslint.config.js` to exclude `dist/`, `build/`, and config files from linting
* [ ] Remove `.eslintignore` file if present
* [ ] Use BEM naming convention and CSS variables in styles
* [ ] Keep styles modular and avoid global styles
* [ ] Use Flexbox or Grid for layout in CSS
* [ ] Add unit tests for custom hooks and utility functions
* [ ] Use modern JavaScript/TypeScript syntax and best practices throughout the codebase

## ✅ DevOps

* [x] Setup Dockerfile for backend
* [x] Create `docker-compose.yml` with Postgres
* [x] Add `.env` file for secrets
* [x] Deploy successfully to Heroku Container
* [x] Setup GitHub Actions for CI/CD

---

### ⏳ In Progress

* Role-based access control
* Error logging and testing strategy
* Custom hooks and code cleanup
* Styling refinement and ESLint/Prettier integration

---

Let me know when you’d like this committed to the repo.
