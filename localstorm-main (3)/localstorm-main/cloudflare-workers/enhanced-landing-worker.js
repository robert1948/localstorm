// CapeControl Enhanced Landing Page Worker - Production Version

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
    
    // Handle app route - redirect or show coming soon
    if (url.pathname === '/app' || url.pathname.startsWith('/app/')) {
      return new Response(`<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CapeControl Dashboard - Coming Soon</title>
    <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>🚁</text></svg>">
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; 
               background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
               color: white; min-height: 100vh; display: flex; align-items: center; justify-content: center; }
        .container { text-align: center; padding: 2rem; }
        .logo { font-size: 3rem; font-weight: bold; margin-bottom: 1rem; }
        .message { font-size: 1.5rem; margin-bottom: 2rem; opacity: 0.9; }
        .btn { display: inline-block; background: white; color: #667eea; padding: 1rem 2rem; 
               text-decoration: none; border-radius: 8px; font-weight: bold; }
    </style>
</head>
<body>
    <div class="container">
        <div class="logo">🚁 CapeControl</div>
        <div class="message">Dashboard Coming Soon</div>
        <p>We're building something amazing for drone operations management.</p>
        <br>
        <a href="/" class="btn">← Back to Home</a>
    </div>
</body>
</html>`, {
        status: 200,
        headers: { 'Content-Type': 'text/html', ...securityHeaders }
      })
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
    
    // Enhanced Landing page
    const landingPage = `<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CapeControl - Professional Drone Operations Management Platform</title>
    <meta name="description" content="Advanced drone fleet management, mission planning, and real-time analytics platform. Streamline your drone operations with CapeControl's comprehensive suite of tools.">
    <meta name="keywords" content="drone management, UAV operations, fleet tracking, mission planning, drone analytics">
    <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>🚁</text></svg>">
    
    <!-- Open Graph / Social Media -->
    <meta property="og:type" content="website">
    <meta property="og:title" content="CapeControl - Drone Operations Management">
    <meta property="og:description" content="Professional drone fleet management and mission planning platform">
    <meta property="og:url" content="https://cape-control.com">
    
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        body { 
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            line-height: 1.6;
            color: #333;
        }
        
        /* Hero Section */
        .hero {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            min-height: 100vh;
            display: flex;
            align-items: center;
            position: relative;
            overflow: hidden;
        }
        
        .hero::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="grid" width="10" height="10" patternUnits="userSpaceOnUse"><path d="M 10 0 L 0 0 0 10" fill="none" stroke="rgba(255,255,255,0.1)" stroke-width="0.5"/></pattern></defs><rect width="100" height="100" fill="url(%23grid)"/></svg>');
            opacity: 0.3;
        }
        
        .container { 
            max-width: 1200px; 
            margin: 0 auto; 
            padding: 2rem; 
            position: relative; 
            z-index: 1;
        }
        
        .hero-content {
            text-align: center;
            max-width: 800px;
            margin: 0 auto;
        }
        
        .logo { 
            font-size: 4rem; 
            font-weight: 800; 
            margin-bottom: 1rem;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        
        .tagline { 
            font-size: 1.8rem; 
            margin-bottom: 2rem; 
            opacity: 0.95;
            font-weight: 300;
        }
        
        .hero-description {
            font-size: 1.2rem;
            margin-bottom: 3rem;
            opacity: 0.9;
            max-width: 600px;
            margin-left: auto;
            margin-right: auto;
        }
        
        /* Status Badge */
        .status { 
            position: fixed; 
            top: 1rem; 
            right: 1rem; 
            background: rgba(40,167,69,0.95); 
            padding: 0.75rem 1.5rem; 
            border-radius: 25px; 
            font-size: 0.9rem;
            font-weight: 600;
            backdrop-filter: blur(10px);
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
            z-index: 1000;
        }
        
        /* Features Grid */
        .features-section {
            padding: 5rem 0;
            background: #f8f9fa;
        }
        
        .section-title {
            text-align: center;
            font-size: 2.5rem;
            font-weight: 700;
            margin-bottom: 1rem;
            color: #2c3e50;
        }
        
        .section-subtitle {
            text-align: center;
            font-size: 1.2rem;
            color: #6c757d;
            margin-bottom: 4rem;
            max-width: 600px;
            margin-left: auto;
            margin-right: auto;
        }
        
        .features { 
            display: grid; 
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr)); 
            gap: 2.5rem; 
            margin-bottom: 3rem;
        }
        
        .feature { 
            background: white;
            padding: 2.5rem; 
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            border: 1px solid #e9ecef;
        }
        
        .feature:hover {
            transform: translateY(-5px);
            box-shadow: 0 20px 40px rgba(0,0,0,0.15);
        }
        
        .feature-icon {
            font-size: 3rem;
            margin-bottom: 1rem;
            display: block;
        }
        
        .feature h3 { 
            font-size: 1.5rem; 
            margin-bottom: 1rem;
            color: #2c3e50;
            font-weight: 600;
        }
        
        .feature p {
            color: #6c757d;
            font-size: 1.1rem;
            line-height: 1.6;
        }
        
        /* CTA Section */
        .cta-section {
            background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
            color: white;
            padding: 4rem 0;
            text-align: center;
        }
        
        .cta { 
            margin-top: 2rem;
        }
        
        .btn { 
            display: inline-block; 
            padding: 1.2rem 2.5rem; 
            text-decoration: none; 
            border-radius: 10px; 
            font-weight: 600;
            font-size: 1.1rem;
            margin: 0.5rem; 
            transition: all 0.3s ease;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        .btn:hover { 
            transform: translateY(-2px); 
            box-shadow: 0 10px 25px rgba(0,0,0,0.2);
        }
        
        .btn-primary { 
            background: white; 
            color: #667eea;
            border: 2px solid white;
        }
        
        .btn-primary:hover { 
            background: #f8f9fa;
            color: #5a67d8;
        }
        
        .btn-secondary {
            background: transparent;
            color: white;
            border: 2px solid rgba(255,255,255,0.5);
        }
        
        .btn-secondary:hover {
            background: rgba(255,255,255,0.1);
            border-color: white;
        }
        
        /* Footer */
        .footer {
            background: #2c3e50;
            color: white;
            padding: 3rem 0;
            text-align: center;
        }
        
        .footer-content {
            max-width: 800px;
            margin: 0 auto;
        }
        
        .footer p {
            margin-bottom: 1rem;
            opacity: 0.8;
        }
        
        .footer-links {
            margin: 2rem 0;
        }
        
        .footer-links a {
            color: #3498db;
            text-decoration: none;
            margin: 0 1rem;
            font-weight: 500;
        }
        
        .footer-links a:hover {
            color: #5dade2;
        }
        
        /* Responsive Design */
        @media (max-width: 768px) {
            .logo { font-size: 3rem; }
            .tagline { font-size: 1.4rem; }
            .hero-description { font-size: 1.1rem; }
            .features { grid-template-columns: 1fr; }
            .feature { padding: 2rem; }
            .section-title { font-size: 2rem; }
            .container { padding: 1rem; }
            .status { 
                position: static; 
                display: inline-block; 
                margin-bottom: 2rem;
            }
        }
        
        /* Animations */
        @keyframes fadeInUp {
            from {
                opacity: 0;
                transform: translateY(30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        .feature {
            animation: fadeInUp 0.6s ease forwards;
        }
        
        .feature:nth-child(2) { animation-delay: 0.1s; }
        .feature:nth-child(3) { animation-delay: 0.2s; }
        .feature:nth-child(4) { animation-delay: 0.3s; }
        .feature:nth-child(5) { animation-delay: 0.4s; }
        .feature:nth-child(6) { animation-delay: 0.5s; }
    </style>
</head>
<body>
    <!-- Hero Section -->
    <section class="hero">
        <div class="status">🟢 System Operational</div>
        
        <div class="container">
            <div class="hero-content">
                <div class="logo">CapeControl</div>
                <div class="tagline">Professional Drone Operations Management Platform</div>
                <div class="hero-description">
                    Streamline your drone operations with comprehensive fleet management, 
                    intelligent mission planning, and real-time analytics. Built for professionals 
                    who demand precision and reliability.
                </div>
                
                <div class="cta">
                    <a href="/app" class="btn btn-primary">Launch Dashboard</a>
                    <a href="/api/health" class="btn btn-secondary">API Status</a>
                </div>
            </div>
        </div>
    </section>
    
    <!-- Features Section -->
    <section class="features-section">
        <div class="container">
            <h2 class="section-title">Comprehensive Drone Management</h2>
            <p class="section-subtitle">
                Everything you need to manage professional drone operations, 
                from single missions to enterprise-scale deployments.
            </p>
            
            <div class="features">
                <div class="feature">
                    <span class="feature-icon">🚁</span>
                    <h3>Fleet Management</h3>
                    <p>Complete drone fleet tracking with maintenance scheduling, performance monitoring, flight hour logging, and comprehensive asset management for optimal operational efficiency.</p>
                </div>
                
                <div class="feature">
                    <span class="feature-icon">🗺️</span>
                    <h3>Mission Planning</h3>
                    <p>Advanced flight path planning with real-time weather integration, no-fly zone awareness, regulatory compliance checking, and automated route optimization.</p>
                </div>
                
                <div class="feature">
                    <span class="feature-icon">📊</span>
                    <h3>Analytics Dashboard</h3>
                    <p>Real-time data visualization, comprehensive flight analytics, performance metrics, operational insights, and detailed reporting for data-driven decisions.</p>
                </div>
                
                <div class="feature">
                    <span class="feature-icon">🔒</span>
                    <h3>Security & Compliance</h3>
                    <p>Enterprise-grade security with full regulatory compliance, detailed audit trails, encrypted data transmission, and role-based access control.</p>
                </div>
                
                <div class="feature">
                    <span class="feature-icon">🌐</span>
                    <h3>Real-time Monitoring</h3>
                    <p>Live tracking capabilities, comprehensive telemetry data collection, instant alert systems, and remote command capabilities for all drone operations.</p>
                </div>
                
                <div class="feature">
                    <span class="feature-icon">⚡</span>
                    <h3>API Integration</h3>
                    <p>Seamless integration with existing systems through our comprehensive RESTful API, webhooks, real-time data streams, and extensive developer tools.</p>
                </div>
            </div>
        </div>
    </section>
    
    <!-- CTA Section -->
    <section class="cta-section">
        <div class="container">
            <h2 class="section-title" style="color: white;">Ready to Transform Your Drone Operations?</h2>
            <p class="section-subtitle" style="color: rgba(255,255,255,0.9);">
                Join leading organizations using CapeControl to optimize their drone operations
            </p>
            
            <div class="cta">
                <a href="/app" class="btn btn-primary">Get Started Now</a>
                <a href="mailto:contact@cape-control.com" class="btn btn-secondary">Contact Sales</a>
            </div>
        </div>
    </section>
    
    <!-- Footer -->
    <footer class="footer">
        <div class="container">
            <div class="footer-content">
                <p><strong>CapeControl</strong> - Professional Drone Operations Management</p>
                <div class="footer-links">
                    <a href="/api/health">API Health</a>
                    <a href="mailto:support@cape-control.com">Support</a>
                    <a href="mailto:contact@cape-control.com">Contact</a>
                </div>
                <p>
                    Powered by Cloudflare Workers • API: <code>cape-control.com/api/</code><br>
                    Last Updated: ${new Date().toLocaleDateString()}
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
