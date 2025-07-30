/**
 * CapeControl Production Worker
 * =============================
 * 
 * Handles all requests to cape-control.com:
 * - API requests: Proxy to Heroku backend with caching
 * - Frontend requests: Serve static content or redirect
 * - Security headers and CORS handling
 */

export default {
  async fetch(request, env, ctx) {
    return handleRequest(request, ctx)
  }
}

async function handleRequest(request, ctx) {
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

  try {
    // Handle CORS preflight requests
    if (request.method === 'OPTIONS') {
      return handleCORS(securityHeaders)
    }
    
    // Handle API requests - proxy to Heroku
    if (url.pathname.startsWith('/api/')) {
      return handleAPIRequest(request, BACKEND_URL, securityHeaders, ctx)
    }
    
    // Handle frontend requests
    return handleFrontendRequest(url, securityHeaders)
    
  } catch (error) {
    console.error('Worker error:', error)
    return new Response(JSON.stringify({
      error: 'Worker Error',
      message: error.message,
      timestamp: new Date().toISOString()
    }), { 
      status: 500,
      headers: {
        'Content-Type': 'application/json',
        ...securityHeaders
      }
    })
  }
}

async function handleAPIRequest(request, backendUrl, securityHeaders, ctx) {
  // Create the backend URL
  const url = new URL(request.url)
  const targetUrl = new URL(url.pathname + url.search, backendUrl)
  
  // Clone the request for the backend
  const backendRequest = new Request(targetUrl.toString(), {
    method: request.method,
    headers: request.headers,
    body: request.body
  })
  
  // Cache GET requests for 5 minutes
  if (request.method === 'GET' && shouldCache(url.pathname)) {
    const cache = caches.default
    const cacheKey = new Request(targetUrl.toString(), {
      method: 'GET',
      headers: request.headers
    })
    
    let response = await cache.match(cacheKey)
    
    if (!response) {
      response = await fetch(backendRequest)
      
      if (response.ok) {
        const responseToCache = response.clone()
        const headers = new Headers(responseToCache.headers)
        headers.set('Cache-Control', 'public, max-age=300')
        headers.set('CF-Cache-Status', 'MISS')
        
        const cachedResponse = new Response(responseToCache.body, {
          status: responseToCache.status,
          statusText: responseToCache.statusText,
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
    // For non-cacheable requests, just proxy
    response = await fetch(backendRequest)
  }
  
  // Add security headers to response
  const newHeaders = new Headers(response.headers)
  Object.entries(securityHeaders).forEach(([key, value]) => {
    newHeaders.set(key, value)
  })
  
  return new Response(response.body, {
    status: response.status,
    statusText: response.statusText,
    headers: newHeaders
  })
}

async function handleFrontendRequest(url, securityHeaders) {
  // For now, return a simple response with info about CapeControl
  // Later, this can serve your actual frontend assets
  
  const html = `
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CapeControl - Developer Platform</title>
    <style>
        body { 
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; 
            margin: 0; padding: 40px; background: #f8fafc; color: #334155;
            display: flex; align-items: center; justify-content: center; min-height: 100vh;
        }
        .container { 
            text-align: center; max-width: 600px; background: white; 
            padding: 60px 40px; border-radius: 12px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);
        }
        h1 { color: #1e40af; margin-bottom: 16px; font-size: 2.5rem; }
        .subtitle { color: #64748b; font-size: 1.2rem; margin-bottom: 32px; }
        .status { 
            background: #dcfce7; color: #166534; padding: 12px 24px; 
            border-radius: 8px; display: inline-block; margin-bottom: 32px;
        }
        .links { display: flex; gap: 16px; justify-content: center; flex-wrap: wrap; }
        .link { 
            background: #1e40af; color: white; padding: 12px 24px; 
            text-decoration: none; border-radius: 8px; font-weight: 500;
        }
        .link:hover { background: #1d4ed8; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 CapeControl</h1>
        <p class="subtitle">Secure, scalable developer platform</p>
        
        <div class="status">✅ System Operational</div>
        
        <p>Your CapeControl platform is running on Cloudflare Workers with:</p>
        <ul style="text-align: left; max-width: 400px; margin: 24px auto;">
            <li>✅ Enhanced authentication & JWT</li>
            <li>✅ Email notifications (Gmail SMTP)</li>
            <li>✅ Role-based access control</li>
            <li>✅ Developer earnings tracking</li>
            <li>✅ Edge caching & security</li>
        </ul>
        
        <div class="links">
            <a href="/api/health" class="link">API Health</a>
            <a href="/api/enhanced/" class="link">Enhanced API</a>
            <a href="https://github.com/robert1948/localstorm" class="link">GitHub</a>
        </div>
        
        <p style="margin-top: 32px; color: #64748b; font-size: 0.9rem;">
            Powered by Cloudflare Workers • Deployed ${new Date().toISOString()}
        </p>
    </div>
</body>
</html>`
  
  return new Response(html, {
    status: 200,
    headers: {
      'Content-Type': 'text/html; charset=UTF-8',
      ...securityHeaders
    }
  })
}

function shouldCache(pathname) {
  // Cache these API endpoints
  const cacheable = [
    '/api/health',
    '/api/enhanced/health',
    '/api/enhanced/',
    '/api/'
  ]
  
  return cacheable.some(path => pathname.includes(path))
}

function handleCORS(securityHeaders) {
  return new Response(null, {
    status: 204,
    headers: securityHeaders
  })
}
