# CapeControl Cloudflare Workers

This directory contains Cloudflare Workers for the CapeControl production deployment.

## Files

### `corrected-worker.js` (PRODUCTION)
The main production worker that:
- Proxies `/api/*` requests to Heroku backend (`https://capecraft-65eeb6ddf78b.herokuapp.com`)
- Serves a professional landing page for all other requests
- Adds security headers (CORS, XSS protection, etc.)
- Implements caching for API endpoints
- Handles CORS preflight requests

### `simple-test-worker.js`
A basic test worker that returns JSON status - useful for testing deployment and routing.

### `api-cache-worker.js`
An enhanced version with additional caching features and error handling.

## Deployment Instructions

1. **Create/Access Cloudflare Worker:**
   - Go to Cloudflare Dashboard → Workers & Pages
   - Create a new worker or edit existing one
   - Copy the code from `corrected-worker.js`

2. **Set up Routes:**
   - Domain: `cape-control.com/*` → worker-name
   - API: `cape-control.com/api/*` → worker-name

3. **DNS Configuration:**
   - A record: `cape-control.com` → `192.0.2.1` (proxied)
   - CNAME: `www` → `cape-control.com` (proxied)
   - CNAME: `api` → `cape-control.com` (proxied)

## Testing

- Main site: `https://cape-control.com/`
- API health: `https://cape-control.com/api/health`
- Backend direct: `https://capecraft-65eeb6ddf78b.herokuapp.com/api/health`

## Features

- **API Proxy**: Seamless proxying to Heroku backend
- **Landing Page**: Professional CapeControl branding
- **Security**: CORS, XSS protection, content type options
- **Caching**: Smart caching for API endpoints
- **Error Handling**: Graceful fallbacks for backend issues
- **Mobile Responsive**: Optimized for all devices

## Current Status

- ✅ Workers created and tested
- ✅ DNS configured
- ✅ Routes set up
- ⚠️ Need to deploy production worker code
- ⚠️ Resolve 522 connection timeout issues

## Troubleshooting

**522 Error**: Connection timeout between Cloudflare and origin
- Check worker deployment status
- Verify route configuration
- Ensure worker code is properly deployed
- Check Cloudflare dashboard for error logs
