/**
 * CapeControl Production Landing Worker - Fixed Version
 * ==================================================== 
 * 
 * This worker now proxies requests to the Heroku backend first,
 * allowing the React app to be served properly with working images.
 */

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url)
    
    // Heroku backend URL
    const BACKEND_URL = 'https://capecraft-65eeb6ddf78b.herokuapp.com'
    
    // Security headers
    const securityHeaders = {
      'X-Content-Type-Options': 'nosniff',
      'X-Frame-Options': 'DENY',
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type, Authorization'
    }
    
    // Handle CORS
    if (request.method === 'OPTIONS') {
      return new Response(null, { status: 204, headers: securityHeaders })
    }
    
    // Handle favicon requests - serve directly to avoid 522 errors
    if (url.pathname === '/favicon.ico') {
      try {
        const faviconResponse = await fetch('https://lightning-s3.s3.us-east-1.amazonaws.com/static/website/img/logo-64x64.png')
        if (faviconResponse.ok) {
          return new Response(faviconResponse.body, {
            status: 200,
            headers: {
              'Content-Type': 'image/png',
              'Cache-Control': 'public, max-age=86400',
              'Access-Control-Allow-Origin': '*',
              ...securityHeaders
            }
          })
        }
      } catch (error) {
        console.error('Favicon fetch error:', error)
      }
      // Fallback to a simple redirect if fetch fails
      return Response.redirect('https://lightning-s3.s3.us-east-1.amazonaws.com/static/website/img/logo-64x64.png', 301)
    }
    
    // Handle app route - show coming soon for platform
    if (url.pathname === '/app' || url.pathname.startsWith('/app/')) {
      return new Response(`<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CapeControl AI Platform - Coming Soon</title>
    <link rel="icon" type="image/png" href="https://lightning-s3.s3.us-east-1.amazonaws.com/static/website/img/logo-64x64.png">
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; 
               background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
               color: white; min-height: 100vh; display: flex; align-items: center; justify-content: center; }
        .container { text-align: center; padding: 2rem; max-width: 600px; }
        .logo { font-size: 3rem; font-weight: bold; margin-bottom: 1rem; }
        .message { font-size: 1.5rem; margin-bottom: 1rem; opacity: 0.9; }
        .subtitle { font-size: 1.1rem; margin-bottom: 2rem; opacity: 0.8; }
        .btn { display: inline-block; background: white; color: #667eea; padding: 1rem 2rem; 
               text-decoration: none; border-radius: 8px; font-weight: bold; margin: 0.5rem; }
        .btn:hover { transform: translateY(-2px); transition: all 0.2s; }
    </style>
</head>
<body>
    <div class="container">
        <div class="logo">🤖 CapeControl AI</div>
        <div class="message">AI-Agents Platform Coming Soon</div>
        <div class="subtitle">We're building something amazing. AI that understands, adapts, and evolves with your needs.</div>
        <a href="/" class="btn">← Back to Home</a>
        <a href="/api/health" class="btn">API Status</a>
    </div>
</body>
</html>`, {
        status: 200,
        headers: { 'Content-Type': 'text/html', ...securityHeaders }
      })
    }
    
    // API requests - proxy to Heroku backend
    if (url.pathname.startsWith('/api/')) {
      try {
        const backendUrl = new URL(url.pathname + url.search, BACKEND_URL)
        const response = await fetch(backendUrl.toString(), {
          method: request.method,
          headers: request.headers,
          body: request.method !== 'GET' ? request.body : null
        })
        
        const newHeaders = new Headers(response.headers)
        Object.entries(securityHeaders).forEach(([key, value]) => {
          newHeaders.set(key, value)
        })
        
        return new Response(response.body, {
          status: response.status,
          headers: newHeaders
        })
      } catch (error) {
        return new Response(JSON.stringify({
          error: 'Backend unavailable',
          message: 'Could not reach CapeControl API'
        }), {
          status: 502,
          headers: { 'Content-Type': 'application/json', ...securityHeaders }
        })
      }
    }
    
    // 🚀 KEY FIX: For ALL other requests (including root /), proxy to Heroku backend FIRST
    // This allows the React app to be served properly with working images
    try {
      const backendUrl = new URL(url.pathname + url.search, BACKEND_URL)
      const response = await fetch(backendUrl.toString(), {
        method: request.method,
        headers: request.headers,
        body: request.method !== 'GET' ? request.body : null
      })
      
      const newHeaders = new Headers(response.headers)
      Object.entries(securityHeaders).forEach(([key, value]) => {
        newHeaders.set(key, value)
      })
      
      return new Response(response.body, {
        status: response.status,
        headers: newHeaders
      })
    } catch (error) {
      console.error('Backend proxy error:', error)
      
      // Only fall back to static HTML if backend is completely unavailable
      return new Response(`<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CapeControl - Backend Unavailable</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; 
               background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
               color: white; min-height: 100vh; display: flex; align-items: center; justify-content: center; }
        .container { text-align: center; padding: 2rem; max-width: 600px; }
        .logo { font-size: 3rem; font-weight: bold; margin-bottom: 1rem; }
        .message { font-size: 1.5rem; margin-bottom: 1rem; opacity: 0.9; }
    </style>
</head>
<body>
    <div class="container">
        <div class="logo">🤖 CapeControl</div>
        <div class="message">Backend Temporarily Unavailable</div>
        <p>We're working to restore service. Please try again in a few moments.</p>
    </div>
</body>
</html>`, {
        status: 503,
        headers: { 'Content-Type': 'text/html', ...securityHeaders }
      })
    }
  }
}
