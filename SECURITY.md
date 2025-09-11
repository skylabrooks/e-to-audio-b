# Security Guidelines

## 🔒 Credential Management

### DO NOT commit credentials to version control
- Service account JSON files
- API keys
- Environment files (.env)
- Private keys

### Secure Setup Instructions

1. **Download your Google Cloud service account JSON file**
2. **Place it OUTSIDE the project directory** (e.g., `C:\credentials\service-account.json`)
3. **Set environment variable:**
   ```bash
   set GOOGLE_APPLICATION_CREDENTIALS=C:\credentials\service-account.json
   ```
4. **Or use individual environment variables in .env file:**
   ```
   GOOGLE_PROJECT_ID=your-project-id
   GOOGLE_PRIVATE_KEY="-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n"
   GOOGLE_CLIENT_EMAIL=your-service-account@your-project.iam.gserviceaccount.com
   ```

## 🛡️ Security Features Implemented

### Backend Security
- ✅ Rate limiting on all API endpoints
- ✅ Input validation and sanitization
- ✅ File upload restrictions (.txt, .md only)
- ✅ CORS configuration for specific origins
- ✅ Security headers (XSS, CSRF protection)
- ✅ Content Security Policy
- ✅ File size limits (16MB max)
- ✅ Secure filename handling

### Rate Limits
- `/api/detect-roles`: 10 requests per minute
- `/api/synthesize`: 5 requests per minute (expensive operation)
- `/api/preview-voice`: 20 requests per minute
- `/api/voices`: 30 requests per minute
- Default: 100 requests per hour

## 🚨 Security Checklist for Production

### Before Deployment
- [ ] Remove all hardcoded credentials
- [ ] Set strong SECRET_KEY
- [ ] Configure ALLOWED_ORIGINS for your domain
- [ ] Enable HTTPS/SSL
- [ ] Set FLASK_DEBUG=False
- [ ] Update all dependencies
- [ ] Run security audit: `npm audit` and `pip-audit`

### Environment Variables Required
```bash
# Required
GOOGLE_APPLICATION_CREDENTIALS=path/to/service-account.json
SECRET_KEY=your-strong-secret-key

# Optional
ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
FLASK_DEBUG=False
PORT=5000
```

## 🔍 Security Monitoring

### Log Monitoring
- All API requests are logged
- Failed authentication attempts
- Rate limit violations
- Input validation failures

### Health Check
- Endpoint: `/health`
- Monitor for service availability

## 📞 Reporting Security Issues

If you discover a security vulnerability, please:
1. Do NOT create a public issue
2. Email the maintainer directly
3. Include detailed steps to reproduce
4. Allow time for patching before disclosure

## 🔄 Regular Security Maintenance

### Monthly Tasks
- [ ] Update dependencies
- [ ] Review access logs
- [ ] Rotate API keys if needed
- [ ] Check for new security advisories

### Quarterly Tasks
- [ ] Security audit
- [ ] Penetration testing
- [ ] Review and update security policies