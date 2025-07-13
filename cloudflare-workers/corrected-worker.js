// CapeControl Production Worker - Copy this to Cloudflare Dashboard

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
        // Create backend URL with original path and query parameters
        const backendUrl = new URL(url.pathname + url.search, BACKEND_URL)
        
        // Create request to backend with same method, headers, and body
        const backendRequest = new Request(backendUrl.toString(), {
          method: request.method,
          headers: request.headers,
          body: request.method !== 'GET' && request.method !== 'HEAD' ? request.body : null
        })
        
        // Fetch from backend
        const response = await fetch(backendRequest)
        
        // Create new response with security headers
        const newHeaders = new Headers(response.headers)
        Object.entries(securityHeaders).forEach(([key, value]) => {
          newHeaders.set(key, value)
        })
        
        // Add cache headers for GET requests
        if (request.method === 'GET' && shouldCache(url.pathname)) {
          newHeaders.set('Cache-Control', 'public, max-age=300')
        }
        
        return new Response(response.body, {
          status: response.status,
          statusText: response.statusText,
          headers: newHeaders
        })
        
      } catch (error) {
        console.error('API proxy error:', error)
        return new Response(JSON.stringify({
          error: 'Backend unavailable',
          message: 'Could not reach CapeControl API',
          details: error.message
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
    <title>CapeControl - Drone Operations Platform</title>
    <meta name="description" content="CapeControl - Professional drone operations management platform for mission planning, fleet management, and analytics.">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white; min-height: 100vh; display: flex; align-items: center;
        }
        .container { max-width: 1200px; margin: 0 auto; padding: 2rem; text-align: center; }
        .logo { font-size: 3.5rem; font-weight: bold; margin-bottom: 1rem; }
        .tagline { font-size: 1.5rem; margin-bottom: 2rem; opacity: 0.9; max-width: 600px; margin-left: auto; margin-right: auto; }
        .features { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 2rem; margin: 3rem 0; }
        .feature { background: rgba(255,255,255,0.1); padding: 2rem; border-radius: 10px; backdrop-filter: blur(10px); }
        .feature h3 { font-size: 1.25rem; margin-bottom: 1rem; }
        .cta { margin-top: 3rem; }
        .btn { 
            display: inline-block; background: rgba(255,255,255,0.2); color: white; 
            padding: 1rem 2rem; text-decoration: none; border-radius: 8px; 
            font-weight: bold; margin: 0.5rem; transition: all 0.2s;
            border: 2px solid rgba(255,255,255,0.3);
        }
        .btn:hover { transform: translateY(-2px); background: rgba(255,255,255,0.3); }
        .btn-primary { background: white; color: #667eea; }
        .btn-primary:hover { background: #f8f9fa; }
        .status { position: fixed; top: 1rem; right: 1rem; background: rgba(40,167,69,0.9); 
                 padding: 0.5rem 1rem; border-radius: 20px; font-size: 0.9rem; }
        .footer { margin-top: 4rem; opacity: 0.7; font-size: 0.9rem; }
        @media (max-width: 768px) {
            .logo { font-size: 2.5rem; }
            .features { grid-template-columns: 1fr; }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="status">🟢 System Operational</div>
        
        <div class="logo">CapeControl</div>
        <div class="tagline">Professional drone operations management platform for mission planning, fleet management, and real-time analytics.</div>
        
        <div class="features">
            <div class="feature">
                <h3>🚁 Fleet Management</h3>
                <p>Comprehensive drone fleet tracking, maintenance scheduling, and performance monitoring with real-time telemetry.</p>
            </div>
            <div class="feature">
                <h3>🗺️ Mission Planning</h3>
                <p>Advanced flight path planning with weather integration, no-fly zone awareness, and regulatory compliance.</p>
            </div>
            <div class="feature">
                <h3>📊 Analytics Dashboard</h3>
                <p>Real-time data visualization, flight analytics, comprehensive reporting, and operational insights.</p>
            </div>
            <div class="feature">
                <h3>🔒 Security & Compliance</h3>
                <p>Enterprise-grade security with full regulatory compliance, audit trails, and encrypted data transmission.</p>
            </div>
            <div class="feature">
                <h3>🌐 Real-time Monitoring</h3>
                <p>Live tracking, telemetry data, instant alerts, and remote command capabilities for all drone operations.</p>
            </div>
            <div class="feature">
                <h3>⚡ API Integration</h3>
                <p>Seamless integration with existing systems through our comprehensive RESTful API and webhooks.</p>
            </div>
        </div>
        
        <div class="cta">
            <a href="/app" class="btn btn-primary">Launch Platform</a>
            <a href="/api/health" class="btn">API Status</a>
            <a href="https://capecraft-65eeb6ddf78b.herokuapp.com" class="btn">Backend Dashboard</a>
        </div>
        
        <div class="footer">
            <p>Powered by Cloudflare Workers • Backend on Heroku • Built with modern web technologies</p>
            <p>API Endpoint: <code>https://cape-control.com/api/</code> • Last Updated: ${new Date().toLocaleString()}</p>
        </div>
    </div>
</body>
</html>`
    
    return new Response(landingPage, {
      status: 200,
      headers: {
        'Content-Type': 'text/html',
        'Cache-Control': 'public, max-age=3600',
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
