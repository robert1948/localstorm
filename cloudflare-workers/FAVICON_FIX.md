# 🔧 URGENT: Fix Favicon 522 Error

## Issue
The favicon is showing a 522 error due to connection timeout between Cloudflare and the S3 origin.

## Solution
I've updated the worker to serve the favicon directly instead of redirecting to S3.

## 🚀 Deploy Fix Now

1. **Copy the updated worker code:**
   ```bash
   # Copy everything from ai-agents-landing-worker.js
   cat /workspaces/localstorm/cloudflare-workers/ai-agents-landing-worker.js
   ```

2. **Update Cloudflare Worker:**
   - You're already in the Cloudflare Dashboard
   - **Select All** (Ctrl+A) in the code editor
   - **Delete** all existing code
   - **Paste** the new updated code
   - **Save and Deploy**

3. **Test the fix:**
   ```bash
   # Should return 200 OK with PNG content
   curl -I https://cape-control.com/favicon.ico
   ```

## 🔍 What Changed

**Before:**
```javascript
// Simple redirect - caused 522 errors
if (url.pathname === '/favicon.ico') {
  return Response.redirect('https://lightning-s3.s3.us-east-1.amazonaws.com/static/website/img/logo-64x64.png', 301)
}
```

**After:**
```javascript
// Direct fetch and serve - no 522 errors
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
  // Fallback to redirect if fetch fails
  return Response.redirect('https://lightning-s3.s3.us-east-1.amazonaws.com/static/website/img/logo-64x64.png', 301)
}
```

## ✅ Benefits

- **No more 522 errors**: Worker fetches favicon directly from S3
- **Better caching**: 24-hour cache with proper PNG headers
- **Fallback safety**: Still redirects if fetch fails
- **Error logging**: Console errors for debugging
- **Same performance**: Cloudflare edge caching still works

## 🧪 Verification

After deployment, the favicon should:
- ✅ Load without 522 errors
- ✅ Display CapeControl logo properly
- ✅ Cache for 24 hours
- ✅ Work on all browsers and devices

Clear your browser cache (Ctrl+Shift+R) after deployment to see the fix immediately.
