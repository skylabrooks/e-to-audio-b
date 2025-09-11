# 🚀 Quick Start Guide

## Prerequisites
- Docker & Docker Compose installed
- Google Cloud service account JSON file
- Windows with curl available

## 1. Setup Environment

```bash
# Copy environment template
copy .env.example .env

# Edit .env with your settings
notepad .env
```

Required settings in `.env`:
```bash
FLASK_ENV=production
SECRET_KEY=your-strong-secret-key
GOOGLE_CREDENTIALS_PATH=C:\path\to\your\service-account.json
ALLOWED_ORIGINS=http://localhost
```

## 2. Deploy Application

```bash
# One-command deployment
deploy-production.bat
```

This will:
- ✅ Run security checks
- ✅ Execute test suite
- ✅ Build Docker images
- ✅ Start all services
- ✅ Verify deployment

## 3. Verify Deployment

```bash
# Comprehensive verification
verify-deployment.bat
```

Expected output:
```
✅ Docker containers running
✅ Backend healthy
✅ Frontend accessible
✅ Redis connected
✅ API endpoints working
✅ Performance monitoring active
✅ Security headers present

ALL TESTS PASSED - Deployment Successful!
```

## 4. Test the Application

### Basic Integration Test
```bash
integration-test.bat
```

### Performance Test
```bash
load-test.bat
```

### Manual Testing
1. Open http://localhost in browser
2. Upload `demo-story.md`
3. Assign voices to characters
4. Generate audiobook
5. Play the result

## 5. Monitor Performance

### Real-time Metrics
```bash
# View system metrics
curl http://localhost:5000/metrics | python -m json.tool
```

### Application Logs
```bash
# View all logs
docker-compose logs -f

# Backend only
docker-compose logs -f backend

# Frontend only  
docker-compose logs -f frontend
```

## Troubleshooting

### Common Issues

**Backend not starting:**
```bash
# Check credentials
echo %GOOGLE_CREDENTIALS_PATH%
dir "%GOOGLE_CREDENTIALS_PATH%"

# Check logs
docker-compose logs backend
```

**Frontend not loading:**
```bash
# Check build
docker-compose logs frontend

# Rebuild if needed
docker-compose build frontend --no-cache
```

**Redis connection failed:**
```bash
# Check Redis
docker ps | findstr redis

# Restart Redis
docker restart etoaudiobook-redis
```

### Performance Issues
```bash
# Check metrics
curl http://localhost:5000/metrics

# Monitor resource usage
docker stats
```

## Production Checklist

- [ ] Environment variables configured
- [ ] Google Cloud credentials secured
- [ ] SSL certificate installed (for HTTPS)
- [ ] Domain name configured
- [ ] Firewall rules set
- [ ] Monitoring alerts configured
- [ ] Backup strategy implemented
- [ ] Load testing completed

## Next Steps

1. **Custom Domain**: Configure your domain name
2. **HTTPS**: Install SSL certificate
3. **Scaling**: Add more backend instances
4. **Monitoring**: Set up external monitoring
5. **Backups**: Implement backup strategy

## Support

- 📖 Full documentation: `README.md`
- 🔧 Deployment guide: `DEPLOYMENT.md`
- 🚀 Performance guide: `PERFORMANCE.md`
- 🔒 Security guide: `SECURITY.md`
- 🧪 Testing guide: `TESTING.md`