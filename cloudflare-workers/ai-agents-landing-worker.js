// CapeControl AI-Agents Platform - Enhanced Landing Page Worker2

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
    
    // For all other requests (including root /), proxy to the Heroku backend first
    // This allows the React app to be served properly
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
      // Fall back to static landing page only if backend is unavailable
    }

    // AI-Agents Platform Landing Page - Fallback only when backend is down
    const landingPage = `<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CapeControl - AI-Agents Platform | Democratizing Artificial Intelligence</title>
    <meta name="description" content="Democratizing artificial intelligence through our platform that bridges human ambition and technological possibility. Access cutting-edge AI-agents while empowering developers to innovate and earn.">
    <meta name="keywords" content="AI agents, artificial intelligence, automation, AI platform, intelligent solutions, AI democratization, machine learning, business AI">
    
    <!-- Open Graph / Social Media -->
    <meta property="og:type" content="website">
    <meta property="og:title" content="CapeControl - AI-Agents Platform">
    <meta property="og:description" content="Democratizing AI through intelligent agents that understand, adapt, and evolve with your needs. Make AI accessible to everyone.">
    <meta property="og:url" content="https://cape-control.com">
    <meta property="og:image" content="https://lightning-s3.s3.us-east-1.amazonaws.com/static/website/img/logo-64x64.png">
    
    <!-- Favicon -->
    <link rel="icon" type="image/png" href="https://lightning-s3.s3.us-east-1.amazonaws.com/static/website/img/logo-64x64.png">
    <link rel="shortcut icon" type="image/png" href="https://lightning-s3.s3.us-east-1.amazonaws.com/static/website/img/logo-64x64.png">
    
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        body { 
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            background: #fff;
        }
        
        /* Navigation Header */
        .navbar {
            background: #4f46e5;
            padding: 1rem 0;
            position: sticky;
            top: 0;
            z-index: 1000;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        
        .nav-container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 2rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .nav-logo {
            display: flex;
            align-items: center;
            color: white;
            text-decoration: none;
            font-size: 1.5rem;
            font-weight: bold;
        }
        
        .nav-logo img {
            width: 32px;
            height: 32px;
            margin-right: 0.5rem;
            border-radius: 6px;
        }
        
        .nav-menu {
            display: flex;
            list-style: none;
            gap: 2rem;
            align-items: center;
        }
        
        .nav-item {
            color: rgba(255,255,255,0.9);
            text-decoration: none;
            padding: 0.5rem 1rem;
            border-radius: 6px;
            transition: all 0.2s ease;
            font-weight: 500;
        }
        
        .nav-item:hover {
            background: rgba(255,255,255,0.1);
            color: white;
        }
        
        .nav-cta {
            background: white;
            color: #4f46e5;
            padding: 0.75rem 1.5rem;
            border-radius: 8px;
            text-decoration: none;
            font-weight: 600;
            transition: all 0.2s ease;
        }
        
        .nav-cta:hover {
            background: #f8fafc;
            transform: translateY(-1px);
        }
        
        /* Main Content */
        .main-content {
            background: white;
            min-height: calc(100vh - 80px);
        }
        
        /* Hero Section */
        .hero {
            padding: 4rem 0 6rem;
            text-align: center;
            background: linear-gradient(135deg, rgba(79,70,229,0.05) 0%, rgba(255,255,255,1) 100%);
        }
        
        .container { 
            max-width: 1200px; 
            margin: 0 auto; 
            padding: 0 2rem; 
        }
        
        .hero-title {
            font-size: 3.5rem;
            font-weight: 700;
            color: #1e293b;
            margin-bottom: 1.5rem;
            line-height: 1.1;
        }
        
        .hero-subtitle {
            font-size: 1.3rem;
            color: #64748b;
            margin-bottom: 3rem;
            max-width: 700px;
            margin-left: auto;
            margin-right: auto;
            line-height: 1.6;
        }
        
        .hero-buttons {
            display: flex;
            gap: 1rem;
            justify-content: center;
            flex-wrap: wrap;
            margin-bottom: 4rem;
        }
        
        .btn {
            display: inline-block;
            padding: 1rem 2rem;
            border-radius: 8px;
            text-decoration: none;
            font-weight: 600;
            font-size: 1rem;
            transition: all 0.2s ease;
            border: 2px solid transparent;
        }
        
        .btn-primary {
            background: #4f46e5;
            color: white;
        }
        
        .btn-primary:hover {
            background: #4338ca;
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(79,70,229,0.3);
        }
        
        .btn-secondary {
            background: #9333ea;
            color: white;
        }
        
        .btn-secondary:hover {
            background: #7c3aed;
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(147,51,234,0.3);
        }
        
        .btn-outline {
            background: transparent;
            color: #4f46e5;
            border-color: #4f46e5;
        }
        
        .btn-outline:hover {
            background: #4f46e5;
            color: white;
            transform: translateY(-2px);
        }
        
        /* Dashboard Section */
        .dashboard-section {
            padding: 4rem 0;
            background: #f8fafc;
        }
        
        .dashboard-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 4rem;
            align-items: center;
        }
        
        .dashboard-info h2 {
            font-size: 2.5rem;
            font-weight: 700;
            color: #1e293b;
            margin-bottom: 1rem;
        }
        
        .dashboard-info p {
            font-size: 1.1rem;
            color: #64748b;
            line-height: 1.7;
        }
        
        .dashboard-visual {
            background: white;
            border-radius: 16px;
            padding: 2rem;
            box-shadow: 0 4px 20px rgba(0,0,0,0.1);
            border: 1px solid #e2e8f0;
        }
        
        .chart-header {
            display: flex;
            align-items: center;
            margin-bottom: 2rem;
        }
        
        .chart-logo {
            width: 40px;
            height: 40px;
            background: #4f46e5;
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-weight: bold;
            margin-right: 1rem;
        }
        
        .chart-title {
            font-size: 1.2rem;
            font-weight: 600;
            color: #1e293b;
        }
        
        .chart-subtitle {
            font-size: 0.9rem;
            color: #64748b;
        }
        
        .chart-container {
            position: relative;
            height: 200px;
            background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
            border-radius: 12px;
            overflow: hidden;
            display: flex;
            align-items: end;
            justify-content: center;
            padding: 1rem;
        }
        
        .growth-line {
            width: 100%;
            height: 100%;
            background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 150"><path d="M20 120 Q80 100 120 80 T200 40 T280 20" stroke="%234f46e5" stroke-width="4" fill="none" stroke-linecap="round"/><circle cx="280" cy="20" r="6" fill="%234f46e5"/></svg>') no-repeat center;
            background-size: 90% 80%;
        }
        
        .metrics {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 1rem;
            margin-top: 2rem;
        }
        
        .metric {
            text-align: center;
            padding: 1rem;
            background: #f8fafc;
            border-radius: 8px;
        }
        
        .metric-value {
            font-size: 1.5rem;
            font-weight: 700;
            color: #4f46e5;
        }
        
        .metric-label {
            font-size: 0.9rem;
            color: #64748b;
            margin-top: 0.25rem;
        }
        
        .ai-agents-list {
            background: #312e81;
            color: white;
            border-radius: 12px;
            padding: 1.5rem;
            margin-top: 2rem;
        }
        
        .ai-agents-list h4 {
            color: white;
            margin-bottom: 1rem;
            font-size: 1.1rem;
        }
        
        .agent-item {
            display: flex;
            align-items: center;
            padding: 0.75rem 0;
            border-bottom: 1px solid rgba(255,255,255,0.1);
        }
        
        .agent-item:last-child {
            border-bottom: none;
        }
        
        .agent-icon {
            margin-right: 1rem;
            font-size: 1.2rem;
        }
        
        .agent-name {
            font-weight: 500;
            font-size: 0.95rem;
        }
        
        /* Footer */
        .footer {
            background: #1e293b;
            color: white;
            padding: 3rem 0 2rem;
            text-align: center;
        }
        
        .footer-content {
            opacity: 0.8;
            font-size: 0.9rem;
            line-height: 1.8;
        }
        
        .footer-links {
            display: flex;
            justify-content: center;
            gap: 2rem;
            margin: 2rem 0;
            flex-wrap: wrap;
        }
        
        .footer-links a {
            color: rgba(255,255,255,0.8);
            text-decoration: none;
            padding: 0.5rem 1rem;
            border-radius: 6px;
            transition: all 0.2s ease;
        }
        
        .footer-links a:hover {
            background: rgba(255,255,255,0.1);
            color: white;
        }
        
        /* Mobile Responsive */
        @media (max-width: 768px) {
            .nav-menu {
                display: none;
            }
            
            .hero-title {
                font-size: 2.5rem;
            }
            
            .hero-subtitle {
                font-size: 1.1rem;
            }
            
            .hero-buttons {
                flex-direction: column;
                align-items: center;
            }
            
            .dashboard-grid {
                grid-template-columns: 1fr;
                gap: 2rem;
            }
            
            .metrics {
                grid-template-columns: 1fr;
            }
            
            .footer-links {
                flex-direction: column;
                gap: 1rem;
            }
        }
    </style>
</head>
<body>
    <!-- Navigation -->
    <nav class="navbar">
        <div class="nav-container">
            <a href="/" class="nav-logo">
                <img src="https://lightning-s3.s3.us-east-1.amazonaws.com/static/website/img/logo-64x64.png" alt="CapeControl">
                CapeControl
            </a>
            <ul class="nav-menu">
                <li><a href="#vision" class="nav-item">Vision</a></li>
                <li><a href="#platform" class="nav-item">Platform</a></li>
                <li><a href="#developers" class="nav-item">Developers</a></li>
                <li><a href="/app" class="nav-item">Login</a></li>
                <li><a href="/app" class="nav-cta">Get Started</a></li>
            </ul>
        </div>
    </nav>

    <div class="main-content">
        <!-- Hero Section -->
        <section class="hero">
            <div class="container">
                <h1 class="hero-title">Where Intelligence Meets Impact—<br>AI Accessible to Everyone.</h1>
                <p class="hero-subtitle">
                    Democratizing artificial intelligence through our platform that bridges 
                    human ambition and technological possibility. Access cutting-edge AI-agents 
                    while empowering developers to innovate and earn.
                </p>
                
                <div class="hero-buttons">
                    <a href="/app" class="btn btn-primary">Get Started Free</a>
                    <a href="#developers" class="btn btn-secondary">Join as Developer</a>
                    <a href="#platform" class="btn btn-outline">See How It Works</a>
                </div>
            </div>
        </section>

        <!-- Dashboard Section -->
        <section class="dashboard-section" id="platform">
            <div class="container">
                <div class="dashboard-grid">
                    <div class="dashboard-info">
                        <h2>CapeControl</h2>
                        <p>
                            Our AI-agents platform revolutionizes how businesses grow and operate. 
                            Experience intelligent automation that adapts to your needs, 
                            learns from interactions, and delivers measurable results across 
                            all aspects of your business operations.
                        </p>
                    </div>
                    
                    <div class="dashboard-visual">
                        <div class="chart-header">
                            <div class="chart-logo">CC</div>
                            <div>
                                <div class="chart-title">CapeControl</div>
                                <div class="chart-subtitle">Business Growth</div>
                            </div>
                        </div>
                        
                        <div class="chart-container">
                            <div class="growth-line"></div>
                        </div>
                        
                        <div class="metrics">
                            <div class="metric">
                                <div class="metric-value">100</div>
                                <div class="metric-label">AI Efficiency</div>
                            </div>
                            <div class="metric">
                                <div class="metric-value">70</div>
                                <div class="metric-label">Automation Rate</div>
                            </div>
                            <div class="metric">
                                <div class="metric-value">40</div>
                                <div class="metric-label">Cost Reduction</div>
                            </div>
                        </div>
                        
                        <div class="ai-agents-list">
                            <h4>🤖 CapeControl</h4>
                            <div class="agent-item">
                                <span class="agent-icon">📧</span>
                                <span class="agent-name">Email Assistant</span>
                            </div>
                            <div class="agent-item">
                                <span class="agent-icon">📈</span>
                                <span class="agent-name">Lead Scorer</span>
                            </div>
                            <div class="agent-item">
                                <span class="agent-icon">📝</span>
                                <span class="agent-name">Content Writer</span>
                            </div>
                            <div class="agent-item">
                                <span class="agent-icon">⚡</span>
                                <span class="agent-name">Task Automator</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </section>
    </div>

    <!-- Footer -->
    <footer class="footer">
        <div class="container">
            <div class="footer-links">
                <a href="/privacy">Privacy Policy</a>
                <a href="/terms">Terms of Service</a>
                <a href="/about">About Us</a>
                <a href="/contact">Contact</a>
                <a href="/api/health">API Status</a>
            </div>
            <div class="footer-content">
                <p><strong>CapeControl AI-Agents Platform</strong></p>
                <p>Powered by Cloudflare Workers • API: <code>cape-control.com/api/</code></p>
                <p>Making AI accessible • Transforming possibilities into realities</p>
                <p style="margin-top: 1rem; font-size: 0.85rem;">
                    Last Updated: ${new Date().toLocaleString()} • 
                    <a href="https://github.com/yourusername/capecontrol" style="color: rgba(255,255,255,0.7);">Open Source</a>
                </p>
            </div>
        </div>
    </footer>
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
