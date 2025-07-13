# CapeControl React App Development

## Setup Options

### Option A: Next.js (Recommended for SEO + Apps)
```bash
# Create Next.js app
npx create-next-app@latest capecontrol-app --typescript --tailwind --app

# Development
cd capecontrol-app
npm run dev        # Local development
npm run build      # Production build
npm run start      # Production server
```

### Option B: Vite + React (Fast Development)
```bash
# Create Vite React app
npm create vite@latest capecontrol-app -- --template react-ts
cd capecontrol-app
npm install
npm run dev        # Local development
npm run build      # Production build
```

### Deployment Options
1. **Vercel** (Recommended for Next.js)
   - Automatic deployments from GitHub
   - Global CDN
   - Serverless functions

2. **Netlify** (Great for static sites)
   - Easy GitHub integration
   - Form handling
   - Edge functions

3. **Cloudflare Pages** (Integrate with Workers)
   - Same infrastructure as your workers
   - Fast global deployment

### Integration with Current Setup
```javascript
// In your Cloudflare Worker
if (url.pathname.startsWith('/app')) {
  // Proxy to React app or redirect
  return Response.redirect('https://capecontrol-app.vercel.app', 302)
}
```
