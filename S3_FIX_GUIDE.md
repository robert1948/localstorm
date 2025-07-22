# S3 Public Access Fix - Multiple Solutions

## Problem
S3 files exist but return 403 Forbidden when accessed publicly.

## Solutions

### Solution 1: Full S3 Public Access Setup (Recommended)

**Prerequisites:**
- AWS CLI installed and configured
- S3 bucket permissions to modify policies

**Steps:**
```bash
# 1. Run the complete setup
./scripts/setup-s3-public-access.sh

# This will:
# - Remove block public access restrictions
# - Apply bucket policy for public reads
# - Upload all files with public-read ACL
```

### Solution 2: Manual AWS Console Fix

**In AWS S3 Console:**

1. **Go to S3 Bucket `lightning-s3`**
2. **Permissions Tab:**
   - Edit "Block public access" → Uncheck all boxes → Save
   - Edit "Bucket policy" → Paste the policy from `scripts/s3-public-read-policy.json`
3. **Objects Tab:**
   - Select all files in `static/website/img/`
   - Actions → "Make public using ACL"

### Solution 3: Individual File Upload with Public Access

**If you only have specific files to fix:**
```bash
# Upload individual files with public read
aws s3 cp client/public/static/landing01.png \
    s3://lightning-s3/static/website/img/landing01.png \
    --acl public-read \
    --content-type image/png
```

### Solution 4: Use CloudFront Distribution (Advanced)

**Create a CloudFront distribution:**
- Origin: `lightning-s3.s3.amazonaws.com`
- Origin Access Control: Yes
- Behavior: Redirect HTTP to HTTPS
- Price Class: Use only North America and Europe

**Then use URLs like:**
```
https://d1234567890.cloudfront.net/static/website/img/landing01.png
```

### Solution 5: Local Development Fallback

**For immediate local development:**

Update your React components to use local static files:
```jsx
// In Hero.jsx
src="/static/landing01.png"  // This works for localhost
```

## Testing

After applying any solution, test with:
```bash
curl -I "https://lightning-s3.s3.amazonaws.com/static/website/img/landing01.png"
# Should return: HTTP/1.1 200 OK
```

## Security Note

Public S3 access means anyone can access these files. Consider:
- Only making necessary files public
- Using CloudFront for better caching and security
- Monitoring access logs
