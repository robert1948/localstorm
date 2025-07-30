// CapeControl Landing Page Worker - Minimal Production Version

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
    
    // Handle favicon requests
    if (url.pathname === '/favicon.ico') {
      return new Response(null, { status: 204 })
    }
    
    // Handle app route - redirect to actual application
    if (url.pathname === '/app' || url.pathname.startsWith('/app/')) {
      return Response.redirect('https://your-actual-app-url.com', 302)
    }
    
    // API requests - proxy to Heroku
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
    
    // Landing page
    const landingPage = `<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CapeControl - Drone Operations Platform</title>
    <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>🚁</text></svg>">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white; min-height: 100vh; display: flex; align-items: center;
        }
        .container { max-width: 1200px; margin: 0 auto; padding: 2rem; text-align: center; }
        .logo { font-size: 3.5rem; font-weight: bold; margin-bottom: 1rem; }
        .tagline { font-size: 1.5rem; margin-bottom: 2rem; opacity: 0.9; }
        .features { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 2rem; margin: 3rem 0; }
        .feature { background: rgba(255,255,255,0.1); padding: 2rem; border-radius: 10px; }
        .feature h3 { font-size: 1.25rem; margin-bottom: 1rem; }
        .cta { margin-top: 3rem; }
        .btn { 
            display: inline-block; background: rgba(255,255,255,0.2); color: white; 
            padding: 1rem 2rem; text-decoration: none; border-radius: 8px; 
            font-weight: bold; margin: 0.5rem; transition: all 0.2s;
        }
        .btn:hover { transform: translateY(-2px); background: rgba(255,255,255,0.3); }
        .btn-primary { background: white; color: #667eea; }
        .status { position: fixed; top: 1rem; right: 1rem; background: rgba(40,167,69,0.9); 
                 padding: 0.5rem 1rem; border-radius: 20px; font-size: 0.9rem; }
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
        <div class="tagline">Professional drone operations management platform</div>
        
        <div class="features">
            <div class="feature">
                <h3>🚁 Fleet Management</h3>
                <p>Comprehensive drone fleet tracking and maintenance scheduling.</p>
            </div>
            <div class="feature">
                <h3>🗺️ Mission Planning</h3>
                <p>Advanced flight path planning with weather integration.</p>
            </div>
            <div class="feature">
                <h3>📊 Analytics Dashboard</h3>
                <p>Real-time data visualization and operational insights.</p>
            </div>
        </div>
        
        <div class="cta">
            <a href="/app" class="btn btn-primary">Launch Platform</a>
            <a href="/api/health" class="btn">API Status</a>
        </div>
        
        <p style="margin-top: 2rem; opacity: 0.7;">
            Powered by Cloudflare Workers • API: cape-control.com/api/
        </p>
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
