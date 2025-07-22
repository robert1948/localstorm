# 🚨 **CRITICAL SECURITY ALERT - Production Settings Issues**

## ⚠️ **DO NOT DEPLOY UNTIL THESE ARE FIXED!**

Based on the production settings audit, there are **CRITICAL SECURITY VULNERABILITIES** that must be addressed before any GitHub updates or deployments.

---

## 🔥 **IMMEDIATE ACTION REQUIRED**

### **1. 🚨 CRITICAL: Insecure SECRET_KEY**
**Current**: `django-insecure-2w#c0xjda#hshvg^8eb=yl@0(gcy*(uipcyg9*okrkh*)z6`
**Issue**: Using Django development key in production!
**Risk**: All JWT tokens, sessions, and crypto operations are compromised

**FIX NOW:**
```bash
# Generate new secure key
python -c "from secrets import token_urlsafe; print(token_urlsafe(64))"

# Set on Heroku
heroku config:set SECRET_KEY="your-new-secure-key-here" -a capecraft
```

### **2. 🚨 CRITICAL: Wrong API URL**
**Current**: `REACT_APP_API_URL=https://cape-control.com/api`
**Issue**: Missing "www" - frontend can't connect to backend
**Risk**: Complete frontend functionality failure

**FIX NOW:**
```bash
heroku config:set REACT_APP_API_URL="https://www.cape-control.com/api" -a capecraft
```

### **3. ⚠️ HIGH PRIORITY: Missing Production Settings**
**Missing**: `DEBUG=False`, `ENV=production`, `CORS_ORIGINS`
**Risk**: Security vulnerabilities and CORS failures

**FIX NOW:**
```bash
heroku config:set DEBUG=False -a capecraft
heroku config:set ENV=production -a capecraft
heroku config:set CORS_ORIGINS="https://www.cape-control.com,https://cape-control.com" -a capecraft
```

---

## 📋 **Complete Fix Commands**

Run these commands in order:

```bash
# 1. Generate and set new SECRET_KEY
NEW_SECRET=$(python -c "from secrets import token_urlsafe; print(token_urlsafe(64))")
heroku config:set SECRET_KEY="$NEW_SECRET" -a capecraft

# 2. Fix API URL
heroku config:set REACT_APP_API_URL="https://www.cape-control.com/api" -a capecraft

# 3. Set production environment
heroku config:set DEBUG=False -a capecraft
heroku config:set ENV=production -a capecraft

# 4. Configure CORS
heroku config:set CORS_ORIGINS="https://www.cape-control.com,https://cape-control.com" -a capecraft

# 5. Clean up ALLOWED_HOSTS
heroku config:set ALLOWED_HOSTS="capecraft.herokuapp.com,cape-control.com,www.cape-control.com" -a capecraft

# 6. Verify changes
heroku config -a capecraft
```

---

## 🔧 **Update Local Development**

After fixing production, update your local `.env`:

```bash
# Update local database URL to match production
DATABASE_URL=postgres://u8h1en29rnu00:p3020c7560854b178b598d2993a2b91173972e98a202f19c9ba981e3bbd89a88c@c3nv2ev86aje4j.cluster-czrs8kj4isg7.us-east-1.rds.amazonaws.com:5432/d2ggg154krfc75
```

---

## ✅ **Post-Fix Verification**

After applying fixes:

1. **Test production site**: https://www.cape-control.com
2. **Check health endpoint**: https://www.cape-control.com/api/health
3. **Verify frontend loads**: Check for API connection errors
4. **Test user registration**: Ensure full functionality works

---

## 🎯 **GitHub Update Safety**

**✅ SAFE TO UPDATE GITHUB AFTER:**
- [ ] New SECRET_KEY generated and set
- [ ] API URL fixed to include www
- [ ] Production environment variables set
- [ ] All verification tests pass

**🚀 GitHub Workflow Status:**
- ✅ Targets correct app: `capecraft`
- ✅ Uses proper deployment method
- ✅ Has appropriate triggers and safety checks

---

## 🚨 **SECURITY NOTE**

The Heroku config output contained sensitive information including:
- OAuth client secrets
- Database credentials  
- API keys
- SMTP passwords

**Recommendation**: After fixing the SECRET_KEY issue, consider rotating other sensitive credentials for maximum security.

**🔥 DEPLOY ONLY AFTER ALL CRITICAL FIXES ARE APPLIED! 🔥**
