# Production Environment Setup Guide

## Critical Production Environment Variables

### Required Heroku Config Vars

The following environment variables MUST be set in Heroku for secure production deployment:

```bash
# Security (CRITICAL - Change these!)
heroku config:set SECRET_KEY="your-super-secure-production-secret-key-here" -a capecraft
heroku config:set JWT_SECRET_KEY="your-jwt-secret-production-key-here" -a capecraft
heroku config:set SESSION_SECRET="your-session-secret-production-key-here" -a capecraft

# Environment
heroku config:set ENVIRONMENT="production" -a capecraft
heroku config:set DEBUG="False" -a capecraft

# CORS and Security
heroku config:set CORS_ORIGINS="https://www.cape-control.com,https://cape-control.com" -a capecraft
heroku config:set ALLOWED_HOSTS="www.cape-control.com,cape-control.com" -a capecraft
heroku config:set FRONTEND_ORIGIN="https://www.cape-control.com" -a capecraft

# API Configuration
heroku config:set API_BASE_URL="https://www.cape-control.com/api" -a capecraft

# Database (Heroku Postgres add-on will set DATABASE_URL automatically)
# heroku addons:create heroku-postgresql:essential-0 -a capecraft

# S3 Configuration (if using S3 for static assets)
heroku config:set AWS_ACCESS_KEY_ID="your-aws-access-key" -a capecraft
heroku config:set AWS_SECRET_ACCESS_KEY="your-aws-secret-key" -a capecraft
heroku config:set AWS_STORAGE_BUCKET_NAME="lightning-s3" -a capecraft
heroku config:set AWS_S3_REGION_NAME="us-east-1" -a capecraft

# Email Configuration (if using email features)
heroku config:set SMTP_SERVER="smtp.gmail.com" -a capecraft
heroku config:set SMTP_PORT="587" -a capecraft
heroku config:set SMTP_USE_TLS="true" -a capecraft
heroku config:set SMTP_USERNAME="your-email@cape-control.com" -a capecraft
heroku config:set SMTP_PASSWORD="your-email-password" -a capecraft
heroku config:set FROM_EMAIL="noreply@cape-control.com" -a capecraft
```

## Verification Commands

```bash
# Check current Heroku config
heroku config -a capecraft

# Test production deployment
heroku logs --tail -a capecraft

# Check app status
heroku ps -a capecraft
```

## Security Checklist

- [ ] SECRET_KEY is set to a strong, unique value (not the development default)
- [ ] DEBUG is set to False
- [ ] DATABASE_URL is using Heroku Postgres (not SQLite)
- [ ] CORS_ORIGINS only includes production domains
- [ ] ALLOWED_HOSTS only includes production domains
- [ ] All sensitive keys are unique production values
- [ ] Email credentials are production-ready
- [ ] S3 credentials are production-ready

## Current Status

❌ **CRITICAL**: Production is currently using development environment variables
❌ **SECURITY RISK**: Development SECRET_KEY in production
❌ **DATABASE**: May be using SQLite instead of PostgreSQL
❌ **CORS**: Development localhost origins may be allowed

## Next Steps

1. Set all required Heroku config vars above
2. Verify PostgreSQL add-on is installed
3. Deploy and test production environment
4. Monitor logs for any configuration issues

## Files Updated

- `.env.production` - Template for production environment variables
- `backend/app/config.py` - Uses Pydantic settings with environment variable aliases
- `app.json` - Heroku app configuration requires SECRET_KEY and FRONTEND_ORIGIN
