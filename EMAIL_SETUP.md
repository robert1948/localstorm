# Email Setup Guide for CapeControl

## Overview
CapeControl has email functionality built-in for:
- **User registration notifications** (sent to admin)
- **Password reset emails** (sent to users)
- **Welcome emails** (Phase 2 onboarding)
- **Developer notifications** (earnings, updates)

## Current Infrastructure
✅ **Cloudflare Email Routing** configured for `cape-control.com`  
✅ **Backend email service** ready (`backend/app/email_service.py`)  
✅ **Email templates** for registration and notifications  

## Setup Options

### Option 1: Gmail SMTP (Recommended for Development)

#### Step 1: Prepare Gmail Account
1. **Enable 2-Factor Authentication**
   - Go to [Google Account Security](https://myaccount.google.com/security)
   - Turn on 2-Step Verification

2. **Generate App Password**
   - Go to Security > App passwords
   - Select "Mail" as the app
   - Copy the 16-character password generated

#### Step 2: Configure Local Environment
Update your `.env` file:
```bash
# Email Configuration
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=zeonita@gmail.com  # Your Gmail address
SMTP_PASSWORD=abcd-efgh-ijkl-mnop  # App password from step 1
FROM_EMAIL=noreply@cape-control.com
ADMIN_EMAIL=zeonita@gmail.com
```

#### Step 3: Configure Heroku Production
```bash
heroku config:set SMTP_HOST=smtp.gmail.com
heroku config:set SMTP_PORT=587
heroku config:set SMTP_USERNAME=zeonita@gmail.com
heroku config:set SMTP_PASSWORD=your-app-password
heroku config:set FROM_EMAIL=noreply@cape-control.com
heroku config:set ADMIN_EMAIL=zeonita@gmail.com
```

### Option 2: Cloudflare Email Workers (Advanced)

For production scale, use Cloudflare Email Workers:
1. Create Email Worker in Cloudflare dashboard
2. Update email service to use Cloudflare API
3. Better deliverability and integration

### Option 3: SendGrid (Production Grade)

For high-volume transactional emails:
1. Create SendGrid account
2. Get API key
3. Update SMTP settings:
   ```bash
   SMTP_HOST=smtp.sendgrid.net
   SMTP_PORT=587
   SMTP_USERNAME=apikey
   SMTP_PASSWORD=your-sendgrid-api-key
   ```

## Testing Email Setup

### Test Locally
```bash
cd /workspaces/localstorm
python -c "
import asyncio
from backend.app.email_service import email_service

async def test_email():
    result = await email_service.send_email(
        to_email='zeonita@gmail.com',
        subject='CapeControl Email Test',
        html_content='<h1>Email is working!</h1><p>CapeControl email system is operational.</p>'
    )
    print(f'Email sent: {result}')

asyncio.run(test_email())
"
```

### Test Registration Notification
```bash
curl -X POST "http://localhost:8000/api/enhanced/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "testpass123",
    "fullName": "Test User",
    "role": "customer"
  }'
```

## Email Features Included

### 1. Registration Notifications
- Sent to admin when new user registers
- Includes user role, email, registration time
- HTML formatted with CapeControl branding

### 2. Password Reset
- Secure password reset tokens
- HTML email with reset link
- Expires after 1 hour

### 3. Welcome Emails
- Sent after Phase 2 profile completion
- Role-specific content (customer vs developer)
- Onboarding guidance

### 4. Developer Notifications
- Earnings updates
- Platform announcements
- Integration opportunities

## Email Templates

All emails use professional HTML templates with:
- CapeControl branding
- Responsive design
- Clear call-to-action buttons
- Consistent styling

## Security Features

- **Rate limiting** on email endpoints
- **Token-based** password resets
- **Input validation** on all email addresses
- **XSS protection** in email content

## Monitoring

- Email send success/failure logging
- Development mode prints emails to console
- Production mode tracks email metrics

## Next Steps

1. **Choose your preferred email option** (Gmail recommended for start)
2. **Configure environment variables** 
3. **Test email functionality**
4. **Deploy to production**
5. **Monitor email delivery**

## Troubleshooting

### Common Issues:
- **Gmail "Less secure apps"**: Use App Password instead
- **Cloudflare routing**: Ensure MX records are correct
- **Heroku config**: Use `heroku config` to verify variables
- **Rate limits**: Gmail has daily send limits

### Debug Mode:
If email credentials are missing, the system prints emails to console instead of sending them, perfect for development.
