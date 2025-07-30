/**
 * CapeControl Production API Handler
 * ==================================
 * 
 * Cloudflare Worker that proxies API requests to Heroku backend
 * with caching, security headers, and performance optimization
 */

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url)
    
    // Your Heroku backend URL
    const BACKEND_URL = 'https://capecraft-65eeb6ddf78b.herokuapp.com'
    
    // Security headers
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
    
    // If this is an API request, proxy to backend
    if (url.pathname.startsWith('/api/')) {
      // Create the backend URL
      const backendUrl = new URL(url.pathname + url.search, BACKEND_URL)
      
      // Clone the request with the new URL
      const backendRequest = new Request(backendUrl.toString(), {
        method: request.method,
        headers: request.headers,
        body: request.body
      })
      
      try {
        // Cache GET requests for 5 minutes
        if (request.method === 'GET' && shouldCache(url.pathname)) {
          const cache = caches.default
          const cacheKey = new Request(backendUrl.toString(), {
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
        
      } catch (error) {
        console.error('Proxy error:', error)
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
    
    // For non-API requests, return worker info
    const response = {
      service: "CapeControl API Handler",
      status: "operational", 
      timestamp: new Date().toISOString(),
      worker_url: url.href,
      backend_url: BACKEND_URL,
      message: "Cloudflare Worker is proxying to CapeControl API"
    }
    
    return new Response(JSON.stringify(response, null, 2), {
      status: 200,
      headers: {
        'Content-Type': 'application/json',
        ...securityHeaders
      }
    })
  }
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
