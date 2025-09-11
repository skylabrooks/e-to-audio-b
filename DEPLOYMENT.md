# 🚀 Production Deployment Guide

## Prerequisites

- Docker & Docker Compose installed
- Google Cloud service account JSON file
- Domain name (for production)
- SSL certificate (recommended)

## Quick Deployment

### 1. Environment Setup
```bash
# Copy environment template
copy .env.example .env

# Edit .env with your values
notepad .env
```

### 2. Credential Setup
```bash
# Set path to your service account file
set GOOGLE_CREDENTIALS_PATH=C:\path\to\your\service-account.json
```

### 3. Deploy
```bash
# Run deployment script
deploy.bat

# Or manually
docker-compose up -d
```

## Production Configuration

### Environment Variables
```bash
FLASK_ENV=production
FLASK_DEBUG=False
SECRET_KEY=your-strong-secret-key
GOOGLE_CREDENTIALS_PATH=/path/to/service-account.json
ALLOWED_ORIGINS=https://yourdomain.com
REDIS_URL=redis://redis:6379
LOG_LEVEL=INFO
```

### SSL/HTTPS Setup
1. Obtain SSL certificate (Let's Encrypt recommended)
2. Update nginx configuration
3. Redirect HTTP to HTTPS

### Domain Configuration
1. Point domain to your server IP
2. Update `ALLOWED_ORIGINS` in .env
3. Update nginx server_name

## Monitoring

### Health Checks
- Backend: `http://your-domain/api/health`
- Frontend: `http://your-domain`

### Logs
```bash
# View all logs
docker-compose logs -f

# View specific service
docker-compose logs -f backend
docker-compose logs -f frontend
```

### Log Files
- Application logs: `Backend/logs/app_YYYYMMDD.log`
- Error logs: `Backend/logs/error_YYYYMMDD.log`

## Scaling

### Horizontal Scaling
```yaml
# In docker-compose.yml
backend:
  deploy:
    replicas: 3
```

### Load Balancing
- Use nginx upstream for multiple backend instances
- Consider external load balancer (AWS ALB, etc.)

## Backup Strategy

### Database Backup
- Redis data is persisted in `redis_data` volume
- Regular snapshots recommended

### Application Backup
- Source code in version control
- Environment configuration backup
- SSL certificates backup

## Security Checklist

- [ ] SSL/HTTPS enabled
- [ ] Firewall configured
- [ ] Rate limiting active
- [ ] Security headers enabled
- [ ] Credentials secured
- [ ] Regular updates scheduled

## Troubleshooting

### Common Issues

**Backend not starting:**
```bash
# Check logs
docker-compose logs backend

# Check credentials
docker-compose exec backend env | grep GOOGLE
```

**Frontend not loading:**
```bash
# Check nginx logs
docker-compose logs frontend

# Verify build
docker-compose exec frontend ls -la /usr/share/nginx/html
```

**Rate limiting issues:**
```bash
# Check Redis connection
docker-compose exec redis redis-cli ping
```

## Performance Optimization

### Backend
- Use gunicorn with multiple workers
- Enable Redis for rate limiting storage
- Implement caching for TTS voices

### Frontend
- Enable gzip compression
- Use CDN for static assets
- Implement service worker for caching

### Database
- Regular Redis maintenance
- Monitor memory usage
- Configure appropriate persistence

## Updates

### Application Updates
```bash
# Pull latest code
git pull

# Rebuild and restart
docker-compose build
docker-compose up -d
```

### Security Updates
```bash
# Update base images
docker-compose pull
docker-compose up -d
```