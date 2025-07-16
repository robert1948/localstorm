# CapeControl Development Workflow

## Local Development Setup

### Prerequisites
- Node.js 18+
- Wrangler CLI (`npm install -g wrangler`)
- Cloudflare account

### Development Commands
```bash
# Install Wrangler CLI
npm install -g wrangler

# Login to Cloudflare
wrangler login

# Create new worker project
wrangler generate cape-control-dev

# Local development with live reload
wrangler dev

# Deploy to staging
wrangler publish --env staging

# Deploy to production
wrangler publish --env production
```

### File Structure
```
cape-control-workers/
├── src/
│   ├── index.js          # Main worker code
│   ├── pages/
│   │   ├── landing.js    # Landing page HTML
│   │   ├── about.js      # About page HTML
│   │   └── contact.js    # Contact page HTML
│   └── utils/
│       ├── headers.js    # Security headers
│       └── router.js     # URL routing
├── wrangler.toml         # Cloudflare config
└── package.json
```

### Environment Variables
```toml
# wrangler.toml
[env.production]
name = "capecontrol-api-zeonita"
vars = { BACKEND_URL = "https://capecraft-65eeb6ddf78b.herokuapp.com" }

[env.staging]
name = "capecontrol-staging"
vars = { BACKEND_URL = "https://your-staging-backend.herokuapp.com" }
```
