# 🚀 CapeAI Integration Guide

## 🎯 Quick Start (15 minutes)

### 1. Backend Setup

#### Install Dependencies
```bash
# Add to requirements.txt
openai>=1.3.0
redis>=4.5.0
python-dotenv>=1.0.0

# Install
pip install -r requirements.txt
```

#### Environment Configuration
```bash
# Add to .env file
OPENAI_API_KEY=your_openai_api_key_here
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=your_redis_password_if_needed

# Optional: Advanced configuration
OPENAI_MODEL=gpt-4
AI_CONVERSATION_HISTORY_LIMIT=10
AI_RATE_LIMIT_PER_MINUTE=30
```

#### Add Route to FastAPI
```python
# backend/app/main.py
from app.routes.cape_ai import router as cape_ai_router

# Add this line with your other router includes
app.include_router(cape_ai_router, prefix="/api")
```

### 2. Frontend Setup

#### Install the Enhanced Hook
```jsx
// client/src/App.jsx or your main layout component
import CapeAIChatEnhanced from './components/CapeAIChatEnhanced';

function App() {
  return (
    <div className="App">
      {/* Your existing components */}
      
      {/* Add CapeAI at the end - it's positioned absolutely */}
      <CapeAIChatEnhanced />
    </div>
  );
}
```

#### Configure API Endpoint
```javascript
// client/src/config.js or .env.local
REACT_APP_API_URL=http://localhost:8000/api

// For production
REACT_APP_API_URL=https://capecraft-65eeb6ddf78b.herokuapp.com/api
```

### 3. Test the Integration

#### Start Services
```bash
# Terminal 1: Start Redis (if not running)
redis-server

# Terminal 2: Start FastAPI backend
cd backend
uvicorn app.main:app --reload --port 8000

# Terminal 3: Start React frontend
cd client
npm start
```

#### Test Conversation
1. Open your React app
2. Click the CapeAI button (🤖) in the bottom-right
3. Type "Hello CapeAI" and press Enter
4. You should get an intelligent AI response!

## 🔧 Advanced Integration

### Database Integration (Optional)

If you want persistent conversation storage in PostgreSQL:

```sql
-- Add to your existing database schema
CREATE TABLE cape_ai_conversations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    session_id VARCHAR(100) NOT NULL,
    message_type VARCHAR(20) NOT NULL, -- 'user' | 'assistant' | 'system'
    content TEXT NOT NULL,
    context_data JSONB,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_cape_ai_user_session ON cape_ai_conversations(user_id, session_id);
CREATE INDEX idx_cape_ai_created_at ON cape_ai_conversations(created_at);

-- AI user profiles for learning
CREATE TABLE cape_ai_user_profiles (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) UNIQUE,
    interaction_patterns JSONB DEFAULT '{}',
    preferences JSONB DEFAULT '{}',
    skill_level VARCHAR(20) DEFAULT 'beginner',
    total_conversations INTEGER DEFAULT 0,
    last_interaction TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

### Enhanced Authentication Integration

```python
# backend/app/routes/cape_ai.py
# Update the existing route to include database storage

from app.database import get_db
from sqlalchemy.orm import Session

@router.post("/prompt", response_model=AIResponse)
async def ai_prompt(
    request: AIPromptRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Your existing code...
    
    # Optional: Save to database for analytics
    if settings.ENABLE_AI_ANALYTICS:
        await save_conversation_to_db(db, current_user.id, session_id, user_message, ai_result)
    
    return AIResponse(...)
```

### Mobile-Optimized Positioning

```jsx
// client/src/components/CapeAIChatEnhanced.jsx
// Add responsive positioning

const getChatPosition = () => {
  const isMobile = window.innerWidth < 768;
  
  return {
    position: 'fixed',
    bottom: isMobile ? '1rem' : '1.5rem',
    right: isMobile ? '1rem' : '1.5rem',
    width: isMobile ? 'calc(100vw - 2rem)' : '24rem',
    maxWidth: isMobile ? 'none' : '90vw',
    zIndex: 9999
  };
};
```

## 🎨 Customization Options

### Custom AI Personality

```python
# backend/app/routes/cape_ai.py
# Modify the _build_system_prompt method

def _build_system_prompt(self, context: Dict[str, Any]) -> str:
    # Your custom personality
    personality = """You are CapeAI, a friendly and knowledgeable assistant for CapeControl.

    Your personality traits:
    - Professional but approachable
    - Expert in AI and automation
    - Patient with beginners
    - Proactive in offering help
    - Focused on practical solutions

    Your expertise areas:
    - AI agent selection and configuration
    - Platform navigation and features
    - Automation workflow design
    - Cost optimization strategies
    - Technical troubleshooting
    """
    
    return personality + context_specific_guidance
```

### Custom UI Theme

```jsx
// client/src/components/CapeAIChatEnhanced.jsx
// Add theme support

const theme = {
  primary: '#667eea',      // Your brand primary color
  secondary: '#764ba2',    // Your brand secondary color
  background: '#ffffff',   // Chat background
  userMessage: '#667eea',  // User message color
  aiMessage: '#f8f9fa',    // AI message background
  text: '#333333',         // Text color
  border: '#e5e7eb'        // Border color
};

// Apply throughout component
className={`bg-${theme.primary} text-white ...`}
```

### Context-Aware Suggestions

```python
# backend/app/routes/cape_ai.py
# Enhance _generate_suggestions method

def _generate_suggestions(self, context: Dict[str, Any], message: str) -> List[str]:
    # Your business-specific suggestions
    user_role = context.get('user_role', 'user')
    current_page = context.get('current_page', '/')
    
    if user_role == 'developer':
        return [
            "Show me API documentation",
            "How do I publish an agent?",
            "Check my developer dashboard"
        ]
    elif user_role == 'business_owner':
        return [
            "Recommend agents for my industry",
            "Show cost optimization tips", 
            "Help me scale my automation"
        ]
    
    # Default suggestions...
```

## 🚀 Production Deployment

### Environment Variables (Heroku/Railway)

```bash
# Required
OPENAI_API_KEY=sk-...your-openai-key
REDIS_URL=redis://your-redis-url

# Optional optimizations
OPENAI_MODEL=gpt-4
AI_RATE_LIMIT_PER_MINUTE=20
AI_CONVERSATION_TTL_DAYS=30
ENABLE_AI_ANALYTICS=true
```

### Cloudflare Worker Integration

```javascript
// cloudflare-workers/enhanced-landing-worker.js
// Add AI chat proxy for better performance

if (url.pathname.startsWith('/api/ai/')) {
  // Proxy AI requests to your backend with caching
  const cacheKey = `ai_cache:${url.pathname}:${await request.text()}`;
  const cached = await env.AI_CACHE.get(cacheKey);
  
  if (cached) {
    return new Response(cached, {
      headers: { 'Content-Type': 'application/json' }
    });
  }
  
  // Forward to backend and cache response
  const response = await fetch(`${BACKEND_URL}${url.pathname}`, {
    method: request.method,
    headers: request.headers,
    body: request.body
  });
  
  if (response.ok) {
    const responseText = await response.text();
    await env.AI_CACHE.put(cacheKey, responseText, { expirationTtl: 300 });
    return new Response(responseText, response);
  }
}
```

### Performance Monitoring

```python
# backend/app/middleware/ai_monitoring.py
import time
from fastapi import Request

async def monitor_ai_performance(request: Request, call_next):
    if request.url.path.startswith("/api/ai/"):
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        
        # Log AI performance metrics
        logger.info(f"AI Request: {request.url.path} took {process_time:.2f}s")
        
        # Optional: Send to analytics service
        if process_time > 5.0:  # Alert on slow responses
            logger.warning(f"Slow AI response: {process_time:.2f}s")
            
        return response
    
    return await call_next(request)
```

## 📊 Analytics & Monitoring

### AI Usage Analytics

```python
# backend/app/services/ai_analytics.py
class AIAnalyticsService:
    def __init__(self):
        self.redis = redis.Redis()
    
    async def track_conversation(self, user_id: str, message_count: int, response_time: float):
        # Track daily usage
        date_key = f"ai_usage:{datetime.now().strftime('%Y-%m-%d')}"
        await self.redis.hincrby(date_key, f"user:{user_id}", message_count)
        await self.redis.expire(date_key, 86400 * 30)  # 30 days
        
        # Track performance
        perf_key = f"ai_performance:{datetime.now().strftime('%Y-%m-%d:%H')}"
        await self.redis.lpush(perf_key, response_time)
        await self.redis.expire(perf_key, 86400 * 7)  # 7 days
    
    async def get_usage_stats(self, days: int = 7) -> dict:
        stats = {}
        for i in range(days):
            date = (datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d')
            daily_usage = await self.redis.hgetall(f"ai_usage:{date}")
            stats[date] = len(daily_usage)  # Number of active users
        return stats
```

### User Satisfaction Tracking

```jsx
// client/src/components/CapeAIChatEnhanced.jsx
// Add rating system

const MessageRating = ({ messageId, onRate }) => (
  <div className="flex items-center space-x-2 mt-2">
    <span className="text-xs text-gray-500">Was this helpful?</span>
    <button 
      onClick={() => onRate(messageId, 'positive')}
      className="text-green-600 hover:text-green-700"
    >
      👍
    </button>
    <button 
      onClick={() => onRate(messageId, 'negative')}
      className="text-red-600 hover:text-red-700"
    >
      👎
    </button>
  </div>
);
```

## 🔍 Troubleshooting

### Common Issues

#### 1. "AI service error: 401"
```bash
# Check your OpenAI API key
echo $OPENAI_API_KEY

# Verify key is valid
curl https://api.openai.com/v1/models \
  -H "Authorization: Bearer $OPENAI_API_KEY"
```

#### 2. "Redis connection failed"
```bash
# Check Redis is running
redis-cli ping

# Should return "PONG"
```

#### 3. "CORS error in browser"
```python
# backend/app/main.py
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://cape-control.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

#### 4. "Chat not appearing on mobile"
```css
/* Check z-index conflicts */
.cape-ai-chat {
  z-index: 9999 !important;
  position: fixed !important;
}
```

### Debug Mode

```python
# backend/app/routes/cape_ai.py
# Add debug logging

import logging
logger = logging.getLogger(__name__)

async def ai_prompt(...):
    logger.debug(f"AI request from user {current_user.id}: {request.message}")
    logger.debug(f"Context: {request.context}")
    
    # ... your code
    
    logger.debug(f"AI response: {ai_result['response']}")
    return AIResponse(...)
```

## 🎯 Success Metrics

Track these KPIs to measure CapeAI success:

### User Engagement
- **Daily Active AI Users**: Users who interact with CapeAI daily
- **Average Session Length**: Time spent in AI conversations
- **Messages per Session**: Conversation depth
- **Retention Rate**: Users returning to use AI features

### AI Performance
- **Response Time**: Average AI response latency (target: < 2s)
- **Response Quality**: User satisfaction ratings
- **Resolution Rate**: % of queries successfully answered
- **Escalation Rate**: % requiring human support

### Business Impact
- **Onboarding Completion**: Increase in guided onboarding completion
- **Feature Adoption**: AI-driven feature discovery and usage
- **Support Ticket Reduction**: Decrease in manual support requests
- **User Conversion**: AI-assisted conversion to paid plans

### Implementation Timeline
- **Week 1**: Basic AI chat working locally ✅
- **Week 2**: Production deployment with Redis ✅ 
- **Week 3**: Advanced features (actions, suggestions) ✅
- **Week 4**: Analytics and optimization ⏳
- **Month 2**: Voice integration and advanced learning 🎯

---

**Congratulations! You now have a production-ready AI assistant that will transform your user experience. CapeAI is ready to help your users succeed! 🚀**
