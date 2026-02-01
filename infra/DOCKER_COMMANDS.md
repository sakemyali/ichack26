# Docker Quick Reference

## 🚀 Quick Start Commands

```bash
# 1. Navigate to infra directory
cd infra

# 2. Verify Docker setup
./verify-docker.sh

# 3. Build and start all services
docker-compose up --build

# 4. Access the application
# - Middleware: http://localhost:8000/docs
# - Backend: http://localhost:8001/docs
# - Database UI: http://localhost:8081
```

## 📦 Build Commands

```bash
# Build all services
docker-compose build

# Build specific service
docker-compose build middleware
docker-compose build backend

# Force rebuild (no cache)
docker-compose build --no-cache
```

## ▶️ Start/Stop Commands

```bash
# Start all services (foreground)
docker-compose up

# Start all services (background)
docker-compose up -d

# Build and start together
docker-compose up --build -d

# Stop all services
docker-compose stop

# Stop and remove containers
docker-compose down

# Stop and remove everything (including volumes)
docker-compose down -v
```

## 🔍 Monitoring Commands

```bash
# View all logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f middleware
docker-compose logs -f backend

# Check service status
docker-compose ps

# View resource usage
docker stats
```

## 🔧 Debug Commands

```bash
# Execute shell in running container
docker-compose exec middleware sh
docker-compose exec backend bash

# Run a one-off command
docker-compose run middleware python -c "import requests; print(requests.__version__)"

# View environment variables
docker-compose exec middleware env

# Restart specific service
docker-compose restart middleware
```

## 🧪 Testing Commands

```bash
# Run backend tests
docker-compose exec backend pytest

# Run with coverage
docker-compose exec backend pytest --cov

# Run specific test file
docker-compose exec backend pytest tests/test_api.py
```

## 🔄 Update Workflow

When you change code:

```bash
# For services with hot-reload (dev mode)
# No rebuild needed - just save the file!

# For production or after dependency changes
docker-compose down
docker-compose up --build -d
```

## 🗑️ Cleanup Commands

```bash
# Remove stopped containers
docker-compose rm

# Remove unused images
docker image prune

# Remove all unused resources
docker system prune

# Nuclear option (remove everything)
docker system prune -a --volumes
```

## 🐛 Troubleshooting

### Port already in use
```bash
# Find what's using port 8000
lsof -i :8000

# Kill the process
kill -9 <PID>

# Or change port in docker-compose.yml
ports:
  - "8002:8000"  # Use 8002 instead of 8000
```

### Container won't start
```bash
# Check logs
docker-compose logs <service-name>

# Inspect container
docker-compose inspect <service-name>

# Remove and rebuild
docker-compose down
docker-compose up --build
```

### Database connection issues
```bash
# Reset database
docker-compose down -v
docker-compose up -d db
sleep 5
docker-compose up -d backend middleware

# Check database logs
docker-compose logs db
```

### Out of disk space
```bash
# Check Docker disk usage
docker system df

# Clean up
docker system prune -a --volumes
```

## 📊 Database Management

```bash
# Backup database
docker-compose exec db pg_dump -U app app > backup.sql

# Restore database
docker-compose exec -T db psql -U app app < backup.sql

# Connect to database
docker-compose exec db psql -U app app

# View database with pgweb
open http://localhost:8081
```

## 🌐 Network Commands

```bash
# List Docker networks
docker network ls

# Inspect network
docker network inspect infra_default

# Test connectivity between services
docker-compose exec middleware ping backend
docker-compose exec backend ping db
```

## 📝 Useful Aliases

Add to your `~/.zshrc`:

```bash
# Docker Compose shortcuts
alias dc='docker-compose'
alias dcu='docker-compose up'
alias dcub='docker-compose up --build'
alias dcd='docker-compose down'
alias dcl='docker-compose logs -f'
alias dcp='docker-compose ps'
alias dcr='docker-compose restart'

# Docker shortcuts
alias di='docker images'
alias dps='docker ps'
alias dpsa='docker ps -a'
```

Then reload: `source ~/.zshrc`

Usage:
```bash
dc build
dcub -d
dcl middleware
```

## 🔐 Environment Variables

### Middleware (.env)
```env
CDSE_CLIENT_ID=your-sentinel-client-id
CDSE_CLIENT_SECRET=your-sentinel-secret
```

### Backend (in docker-compose.yml)
```yaml
environment:
  DATABASE_URL: postgresql+psycopg://app:app@db:5432/app
  ENV: dev
```

### Override in docker-compose
```bash
# Set env var for specific run
BACKEND_URL=http://custom-backend:9000 docker-compose up
```

## 📈 Production Tips

1. **Remove hot-reload**: Change CMD to use `--workers 4` instead of `--reload`
2. **Use tagged images**: Tag and version your images
3. **Resource limits**: Add CPU/memory limits to services
4. **Health checks**: Add health check configurations
5. **Logging**: Configure proper log drivers
6. **Secrets**: Use Docker secrets instead of .env files
7. **Multi-stage builds**: Reduce image size

Example production config:
```yaml
middleware:
  image: myregistry/middleware:1.0.0
  deploy:
    replicas: 3
    resources:
      limits:
        cpus: '0.5'
        memory: 512M
  healthcheck:
    test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
    interval: 30s
    timeout: 10s
    retries: 3
```
