/**
 * CapeControl Production Worker
 * ============================
 * 
 * Handles all requests to cape-control.com:
 * - Proxies API requests to Heroku backend
 * - Serves frontend landing page
 * - Provides security headers and caching
 */

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url)
    
    // Your Heroku backend URL
    const BACKEND_URL = 'https://capecraft-65eeb6ddf78b.herokuapp.com'
    
    // Security headers for all responses
    const securityHeaders = {
      'X-Content-Type-Options': 'nosniff',
      'X-Frame-Options': 'DENY',
      'X-XSS-Protection': '1; mode=block',
      'Referrer-Policy': 'strict-origin-when-cross-origin',
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type, Authorization, X-Requested-With'
    }
    
    // Handle CORS preflight
    if (request.method === 'OPTIONS') {
      return new Response(null, {
        status: 204,
        headers: securityHeaders
      })
    }
    
    // API requests - proxy to Heroku backend
    if (url.pathname.startsWith('/api/')) {
      try {
        // Create backend URL
        const backendUrl = new URL(url.pathname + url.search, BACKEND_URL)
        
        // Create request to backend
        const backendRequest = new Request(backendUrl.toString(), {
          method: request.method,
          headers: request.headers,
          body: request.body
        })
        
        // For cacheable GET requests
        if (request.method === 'GET' && shouldCache(url.pathname)) {
          const cache = caches.default
          const cacheKey = new Request(backendUrl.toString())
          
          let response = await cache.match(cacheKey)
          
          if (!response) {
            response = await fetch(backendRequest)
            
            if (response.ok) {
              const headers = new Headers(response.headers)
              headers.set('Cache-Control', 'public, max-age=300')
              headers.set('CF-Cache-Status', 'MISS')
              
              const cachedResponse = new Response(response.body, {
                status: response.status,
                statusText: response.statusText,
                headers: headers
              })
              
              ctx.waitUntil(cache.put(cacheKey, cachedResponse.clone()))
              response = cachedResponse
            }
          } else {
            const headers = new Headers(response.headers)
            headers.set('CF-Cache-Status', 'HIT')
            response = new Response(response.body, {
              status: response.status,
              statusText: response.statusText,
              headers: headers
            })
          }
        } else {
          // For non-cacheable requests
          response = await fetch(backendRequest)
        }
        
        // Add security headers
        const newHeaders = new Headers(response.headers)
        Object.entries(securityHeaders).forEach(([key, value]) => {
          newHeaders.set(key, value)
        })
        
        return new Response(response.body, {
          status: response.status,
          statusText: response.statusText,
          headers: newHeaders
        })
        
      } catch (error) {
        console.error('API proxy error:', error)
        return new Response(JSON.stringify({
          error: 'Backend unavailable',
          message: 'Could not reach CapeControl API'
        }), {
          status: 502,
          headers: {
            'Content-Type': 'application/json',
            ...securityHeaders
          }
        })
      }
    }
    
    // Frontend requests - serve landing page
    const landingPage = `<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CapeControl - Advanced API Management Platform</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white; min-height: 100vh; display: flex; align-items: center;
        }
        .container { max-width: 1200px; margin: 0 auto; padding: 2rem; text-align: center; }
        .logo { font-size: 3rem; font-weight: bold; margin-bottom: 1rem; }
        .tagline { font-size: 1.5rem; margin-bottom: 2rem; opacity: 0.9; }
        .features { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 2rem; margin: 3rem 0; }
        .feature { background: rgba(255,255,255,0.1); padding: 2rem; border-radius: 10px; backdrop-filter: blur(10px); }
        .feature h3 { font-size: 1.25rem; margin-bottom: 1rem; }
        .cta { margin-top: 3rem; }
        .btn { 
            display: inline-block; background: #ff6b6b; color: white; padding: 1rem 2rem; 
            text-decoration: none; border-radius: 5px; font-weight: bold; margin: 0.5rem;
            transition: transform 0.2s;
        }
        .btn:hover { transform: translateY(-2px); }
        .status { position: fixed; top: 1rem; right: 1rem; background: rgba(0,255,0,0.2); 
                 padding: 0.5rem 1rem; border-radius: 20px; font-size: 0.9rem; }
    </style>
</head>
<body>
    <div class="container">
        <div class="status">🟢 System Operational</div>
        
        <div class="logo">🛡️ CapeControl</div>
        <div class="tagline">Advanced API Management & Security Platform</div>
        
        <div class="features">
            <div class="feature">
                <h3>🔐 Enhanced Authentication</h3>
                <p>JWT-based secure authentication with role-based access control and audit logging</p>
            </div>
            <div class="feature">
                <h3>⚡ Edge Performance</h3>
                <p>Global CDN with intelligent caching and 200+ edge locations worldwide</p>
            </div>
            <div class="feature">
                <h3>💰 Developer Earnings</h3>
                <p>Built-in revenue tracking and earnings management for API developers</p>
            </div>
        </div>
        
        <div class="cta">
            <a href="/api/health" class="btn">API Status</a>
            <a href="/api/enhanced/" class="btn">Enhanced API</a>
            <a href="https://capecraft-65eeb6ddf78b.herokuapp.com" class="btn">Dashboard</a>
        </div>
        
        <p style="margin-top: 2rem; opacity: 0.7;">
            Powered by Cloudflare Workers • Deployed on Heroku • Built with ❤️
        </p>
    </div>
</body>
</html>`
    
    return new Response(landingPage, {
      status: 200,
      headers: {
        'Content-Type': 'text/html',
        ...securityHeaders
      }
    })
  }
}

function shouldCache(pathname) {
  // Cache these API endpoints for 5 minutes
  const cacheable = [
    '/api/health',
    '/api/enhanced/health',
    '/api/enhanced/',
    '/api/'
  ]
  
  return cacheable.some(path => pathname.includes(path))
}
