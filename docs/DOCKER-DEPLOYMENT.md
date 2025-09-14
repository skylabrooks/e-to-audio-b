# 🐳 Docker Deployment Guide

This guide will help you deploy EtoAudioBook using Docker containers.

## Prerequisites

- Docker Desktop installed and running
- Google Cloud service account JSON file
- Basic understanding of Docker and command line

## Quick Start

### 1. Prepare Credentials
Place your Google Cloud service account JSON file at:
```
Backend/credentials/service-account.json
```

### 2. Deploy with One Command
**Windows:**
```bash
docker-deploy.bat
```

**Linux/macOS:**
```bash
chmod +x docker-deploy.sh
./docker-deploy.sh
```

### 3. Access Your Application
- **Frontend**: http://localhost
- **Backend API**: http://localhost:5000
- **Health Check**: http://localhost:5000/health

## Manual Deployment

### 1. Environment Setup
Copy and customize the environment file:
```bash
cp .env.example .env
```

Edit `.env` with your specific values:
```env
SECRET_KEY=your-strong-secret-key-here
GOOGLE_CREDENTIALS_PATH=./Backend/credentials/service-account.json
ALLOWED_ORIGINS=http://localhost,http://localhost:3000
```

### 2. Build and Run
```bash
# Stop any existing containers
docker-compose down

# Build and start all services
docker-compose up --build -d

# Check status
docker-compose ps
```

## Services Overview

The deployment includes three services:

### Backend (Flask API)
- **Port**: 5000
- **Container**: etoaudiobook-backend
- **Health Check**: http://localhost:5000/health

### Frontend (React + Nginx)
- **Port**: 80
- **Container**: etoaudiobook-frontend
- **URL**: http://localhost

### Redis (Caching & Rate Limiting)
- **Port**: 6379 (internal)
- **Container**: etoaudiobook-redis
- **Data**: Persisted in Docker volume

## Verification

### Check Deployment Status
```bash
check-deployment.bat  # Windows
```

### View Logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f redis
```

### Test API Endpoints
```bash
# Health check
curl http://localhost:5000/health

# Available voices
curl http://localhost:5000/api/voices
```

## Management Commands

### Stop Services
```bash
docker-compose down
```

### Restart Services
```bash
docker-compose restart
```

### Update Application
```bash
# Pull latest changes
git pull

# Rebuild and restart
docker-compose up --build -d
```

### View Resource Usage
```bash
docker stats
```

## Cleanup

### Remove Containers Only
```bash
docker-compose down
```

### Full Cleanup (including images and volumes)
```bash
docker-cleanup.bat  # Windows
```

Or manually:
```bash
# Stop containers
docker-compose down

# Remove images
docker rmi etoaudiobook-copy_backend etoaudiobook-copy_frontend

# Remove volumes (this will delete Redis data)
docker volume rm etoaudiobook-copy_redis_data
```

## Troubleshooting

### Common Issues

**1. Docker not running**
```
Error: Docker is not running
```
- Start Docker Desktop
- Wait for it to fully initialize

**2. Port already in use**
```
Error: Port 80 is already in use
```
- Stop other web servers (IIS, Apache, etc.)
- Or change ports in docker-compose.yml

**3. Credentials not found**
```
Error: Google Cloud service account credentials not found
```
- Ensure `Backend/credentials/service-account.json` exists
- Check file permissions

**4. Backend health check fails**
```
Backend: Not responding
```
- Check backend logs: `docker-compose logs backend`
- Verify credentials are valid
- Ensure Google Cloud TTS API is enabled

### Debug Commands

```bash
# Check container status
docker-compose ps

# View detailed logs
docker-compose logs -f backend

# Execute commands in container
docker exec -it etoaudiobook-backend bash

# Check Redis connection
docker exec etoaudiobook-redis redis-cli ping
```

## Production Considerations

### Security
- Change default SECRET_KEY in production
- Use proper SSL certificates
- Configure firewall rules
- Use Docker secrets for sensitive data

### Performance
- Increase worker count in production
- Configure Redis persistence
- Set up log rotation
- Monitor resource usage

### Scaling
- Use Docker Swarm or Kubernetes for multi-node deployment
- Configure load balancer
- Set up database clustering
- Implement proper backup strategy

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `SECRET_KEY` | Flask secret key | Required |
| `GOOGLE_CREDENTIALS_PATH` | Path to service account JSON | Required |
| `ALLOWED_ORIGINS` | CORS allowed origins | `http://localhost` |
| `REDIS_URL` | Redis connection URL | `redis://redis:6379` |
| `FLASK_ENV` | Flask environment | `production` |
| `LOG_LEVEL` | Logging level | `INFO` |

## Support

If you encounter issues:
1. Check the logs: `docker-compose logs -f`
2. Verify all prerequisites are met
3. Ensure credentials are properly configured
4. Check Docker Desktop is running and updated

For more help, refer to the main README.md or create an issue in the repository.