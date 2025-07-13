// CapeControl AI-Agents Platform - Enhanced Landing Page Worker

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
    
    // AI-Agents Platform Landing Page
    const landingPage = `<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CapeControl - AI-Agents Platform | Democratizing Artificial Intelligence</title>
    <meta name="description" content="CapeControl empowers everyone with accessible AI-agents. Transform ideas into reality with intelligent automation, personalized solutions, and cutting-edge technology. Register today for AI that evolves with you.">
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
            animation: fadeInUp 1s ease-out;
        }
        
        .logo { 
            font-size: 4rem; 
            font-weight: bold; 
            margin-bottom: 1rem;
            background: linear-gradient(45deg, #fff, #f0f0f0);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        
        .tagline { 
            font-size: 1.8rem; 
            margin-bottom: 1rem; 
            opacity: 0.95;
            font-weight: 300;
        }
        
        .subtitle { 
            font-size: 1.2rem; 
            margin-bottom: 3rem; 
            opacity: 0.85;
            max-width: 800px;
            margin-left: auto;
            margin-right: auto;
        }
        
        .status { 
            position: fixed; 
            top: 1rem; 
            right: 1rem; 
            background: rgba(40,167,69,0.9); 
            padding: 0.75rem 1.5rem; 
            border-radius: 25px; 
            font-size: 0.9rem;
            backdrop-filter: blur(10px);
            animation: pulse 2s infinite;
        }
        
        /* Features Section */
        .features { 
            display: grid; 
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr)); 
            gap: 2rem; 
            margin: 4rem 0; 
        }
        
        .feature { 
            background: rgba(255,255,255,0.1); 
            padding: 2.5rem; 
            border-radius: 15px; 
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255,255,255,0.2);
            transition: all 0.3s ease;
        }
        
        .feature:hover { 
            transform: translateY(-5px); 
            background: rgba(255,255,255,0.15);
        }
        
        .feature-icon { 
            font-size: 3rem; 
            margin-bottom: 1rem; 
            display: block; 
        }
        
        .feature h3 { 
            font-size: 1.4rem; 
            margin-bottom: 1rem; 
            color: #fff;
        }
        
        .feature p { 
            opacity: 0.9; 
            line-height: 1.7;
        }
        
        /* Call-to-Action */
        .cta { 
            margin-top: 4rem;
            text-align: center;
        }
        
        .btn { 
            display: inline-block; 
            background: rgba(255,255,255,0.2); 
            color: white; 
            padding: 1.2rem 2.5rem; 
            text-decoration: none; 
            border-radius: 10px; 
            font-weight: 600; 
            margin: 0.5rem; 
            transition: all 0.3s ease;
            border: 2px solid rgba(255,255,255,0.3);
            font-size: 1.1rem;
        }
        
        .btn:hover { 
            transform: translateY(-3px); 
            background: rgba(255,255,255,0.3);
            box-shadow: 0 10px 25px rgba(0,0,0,0.2);
        }
        
        .btn-primary { 
            background: white; 
            color: #667eea; 
            border-color: white;
        }
        
        .btn-primary:hover { 
            background: #f8f9fa; 
        }
        
        /* Vision Section */
        .vision {
            background: rgba(255,255,255,0.05);
            padding: 3rem 0;
            margin-top: 4rem;
            border-radius: 20px;
            border: 1px solid rgba(255,255,255,0.1);
        }
        
        .vision-content {
            text-align: center;
            max-width: 900px;
            margin: 0 auto;
        }
        
        .vision h2 {
            font-size: 2.5rem;
            margin-bottom: 1.5rem;
            background: linear-gradient(45deg, #fff, #f0f0f0);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        
        .vision-points {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 2rem;
            margin-top: 3rem;
        }
        
        .vision-point {
            text-align: left;
            padding: 1.5rem;
            background: rgba(255,255,255,0.08);
            border-radius: 10px;
            border-left: 4px solid rgba(255,255,255,0.3);
        }
        
        .vision-point h4 {
            font-size: 1.2rem;
            margin-bottom: 0.8rem;
            color: #fff;
        }
        
        .vision-point p {
            opacity: 0.9;
            font-size: 0.95rem;
            line-height: 1.6;
        }
        
        /* Footer */
        .footer { 
            margin-top: 4rem; 
            padding-top: 2rem;
            border-top: 1px solid rgba(255,255,255,0.2);
            text-align: center;
        }
        
        .footer-content {
            opacity: 0.8; 
            font-size: 0.95rem;
            line-height: 1.8;
        }
        
        .footer-links {
            margin: 1rem 0;
        }
        
        .footer-links a {
            color: rgba(255,255,255,0.9);
            text-decoration: none;
            margin: 0 1rem;
            padding: 0.5rem 1rem;
            border-radius: 5px;
            transition: all 0.2s ease;
        }
        
        .footer-links a:hover {
            background: rgba(255,255,255,0.1);
        }
        
        /* Animations */
        @keyframes fadeInUp {
            from { opacity: 0; transform: translateY(30px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        @keyframes pulse {
            0%, 100% { opacity: 0.9; }
            50% { opacity: 1; }
        }
        
        /* Mobile Responsive */
        @media (max-width: 768px) {
            .logo { font-size: 2.8rem; }
            .tagline { font-size: 1.4rem; }
            .subtitle { font-size: 1rem; }
            .features { grid-template-columns: 1fr; }
            .vision-points { grid-template-columns: 1fr; }
            .container { padding: 1rem; }
            .btn { padding: 1rem 2rem; font-size: 1rem; }
        }
    </style>
</head>
<body>
    <div class="hero">
        <div class="status">🤖 AI-Agents Operational</div>
        
        <div class="container">
            <div class="hero-content">
                <div class="logo">CapeControl</div>
                <div class="tagline">Democratizing Artificial Intelligence</div>
                <div class="subtitle">
                    Where intelligence meets impact, and possibilities become realities. 
                    Our AI-agents bridge human ambition and technological possibility, 
                    making advanced AI accessible to everyone.
                </div>
                
                <div class="features">
                    <div class="feature">
                        <span class="feature-icon">🧠</span>
                        <h3>Intelligent AI-Agents</h3>
                        <p>AI that goes beyond automation. Our agents understand context, anticipate needs, and continuously learn from interactions to provide personalized, actionable solutions.</p>
                    </div>
                    <div class="feature">
                        <span class="feature-icon">🚀</span>
                        <h3>Empowerment Through Accessibility</h3>
                        <p>From startups to enterprises, solo entrepreneurs to creative individuals - democratizing AI technology for users of all technical backgrounds and resources.</p>
                    </div>
                    <div class="feature">
                        <span class="feature-icon">⚡</span>
                        <h3>Adaptability & Evolution</h3>
                        <p>Built to evolve with changing needs, market trends, and technological advancements. Our platform ensures you remain agile and competitive.</p>
                    </div>
                    <div class="feature">
                        <span class="feature-icon">🎯</span>
                        <h3>Simplicity in Complexity</h3>
                        <p>Advanced technology made intuitive. Streamlined interfaces and clear processes that deliver value without unnecessary complexity.</p>
                    </div>
                    <div class="feature">
                        <span class="feature-icon">🔧</span>
                        <h3>Productivity Unleashed</h3>
                        <p>Automate repetitive tasks, gain deep insights, and explore innovative approaches. Focus on strategic growth while our AI handles the details.</p>
                    </div>
                    <div class="feature">
                        <span class="feature-icon">🌟</span>
                        <h3>Living AI Demonstration</h3>
                        <p>Experience our platform as a showcase of AI excellence. Every interaction demonstrates the transformative potential of intelligent automation.</p>
                    </div>
                </div>
                
                <div class="vision">
                    <div class="vision-content">
                        <h2>Our Vision</h2>
                        <p style="font-size: 1.2rem; opacity: 0.9; margin-bottom: 2rem;">
                            A world where artificial intelligence is accessible to everyone, transforming ideas into reality 
                            through seamless, intuitive experiences that amplify human potential.
                        </p>
                        
                        <div class="vision-points">
                            <div class="vision-point">
                                <h4>🎯 Client-Centric Design</h4>
                                <p>Intuitive registration and personalized AI-agent capabilities with secure, role-based access and JWT authentication.</p>
                            </div>
                            <div class="vision-point">
                                <h4>📈 Continuous Evolution</h4>
                                <p>AI-agents that learn from every interaction, staying at the forefront of innovation with regular updates.</p>
                            </div>
                            <div class="vision-point">
                                <h4>🌍 Global Impact</h4>
                                <p>Scalable solutions serving diverse users with flexible pricing, from free tiers to premium subscriptions.</p>
                            </div>
                            <div class="vision-point">
                                <h4>🔒 Enterprise Security</h4>
                                <p>Production-ready infrastructure with advanced authentication, audit logging, and 24/7 reliability.</p>
                            </div>
                        </div>
                    </div>
                </div>
                
                <div class="cta">
                    <a href="/app" class="btn btn-primary">Experience AI-Agents</a>
                    <a href="/api/health" class="btn">Platform Status</a>
                    <a href="mailto:hello@cape-control.com" class="btn">Get in Touch</a>
                </div>
                
                <div class="footer">
                    <div class="footer-links">
                        <a href="/privacy">Privacy Policy</a>
                        <a href="/terms">Terms of Service</a>
                        <a href="/about">About Us</a>
                        <a href="/contact">Contact</a>
                    </div>
                    <div class="footer-content">
                        <p><strong>CapeControl AI-Agents Platform</strong></p>
                        <p>Powered by Cloudflare Workers • API: <code>cape-control.com/api/</code></p>
                        <p>Making AI accessible • Transforming possibilities into realities</p>
                        <p style="margin-top: 1rem; font-size: 0.9rem;">
                            Last Updated: ${new Date().toLocaleString()} • 
                            <a href="https://github.com/yourusername/capecontrol" style="color: rgba(255,255,255,0.8);">Open Source</a>
                        </p>
                    </div>
                </div>
            </div>
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
