# Docker Deployment Guide

This guide explains how to run the entire application stack using Docker Compose.

## Architecture

The application consists of four services:
- **middleware** (port 8000): Main API gateway that orchestrates all services
- **backend** (port 8001): RUSLE computation and ML models
- **db** (port 5432): PostgreSQL database
- **pgweb** (port 8081): Database web interface

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2.0+

## Quick Start

1. **Navigate to the infrastructure directory**:
   ```bash
   cd infra
   ```

2. **Start all services**:
   ```bash
   docker-compose up --build
   ```

3. **Access the services**:
   - Middleware API: http://localhost:8000
   - Backend API: http://localhost:8001
   - Database UI: http://localhost:8081
   - API Docs (Middleware): http://localhost:8000/docs
   - API Docs (Backend): http://localhost:8001/docs

## Environment Configuration

### Middleware

Create `/middleware/.env` with your Copernicus credentials:
```env
CDSE_CLIENT_ID=your-client-id
CDSE_CLIENT_SECRET=your-client-secret
```

### Backend

The backend service automatically connects to the PostgreSQL database using:
```env
DATABASE_URL=postgresql+psycopg://app:app@db:5432/app
```

## Docker Commands

### Build and Start
```bash
# Build images and start all services
docker-compose up --build

# Start in detached mode (background)
docker-compose up -d --build
```

### Stop Services
```bash
# Stop all services
docker-compose down

# Stop and remove volumes (deletes database data)
docker-compose down -v
```

### View Logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f middleware
docker-compose logs -f backend
```

### Rebuild Single Service
```bash
# Rebuild only middleware
docker-compose up --build middleware

# Rebuild only backend
docker-compose up --build backend
```

### Execute Commands in Container
```bash
# Backend shell
docker-compose exec backend bash

# Middleware shell
docker-compose exec middleware bash

# Run tests in backend
docker-compose exec backend pytest
```

## Development Mode

The docker-compose configuration includes volume mounts for hot-reloading:

- **Middleware**: `/middleware` → `/app` (auto-reload on code changes)
- **Backend**: `/backend/app` → `/app/app` (auto-reload on code changes)

This means you can edit code locally and changes will be reflected immediately without rebuilding.

## Testing the API

Once services are running, test the complete pipeline:

```bash
curl -X POST http://localhost:8000/polygon \
  -H "Content-Type: application/json" \
  -d '{
    "type": "Feature",
    "geometry": {
      "type": "Polygon",
      "coordinates": [[[-1.5, 52.0], [-1.4, 52.0], [-1.45, 52.05], [-1.5, 52.0]]]
    },
    "properties": {}
  }'
```

## Troubleshooting

### Port Conflicts
If ports are already in use:
```bash
# Check what's using the port
lsof -i :8000
lsof -i :8001

# Kill the process
kill -9 <PID>
```

### Container Not Starting
```bash
# Check container status
docker-compose ps

# View detailed logs
docker-compose logs <service-name>

# Restart specific service
docker-compose restart <service-name>
```

### Database Issues
```bash
# Reset database
docker-compose down -v
docker-compose up -d db

# Check database logs
docker-compose logs db
```

### Build Cache Issues
```bash
# Force rebuild without cache
docker-compose build --no-cache

# Remove all images and rebuild
docker-compose down --rmi all
docker-compose up --build
```

## Production Deployment

For production, modify the docker-compose.yml:

1. Remove `--reload` from CMD in Dockerfiles
2. Set appropriate resource limits
3. Use environment-specific .env files
4. Add health checks
5. Configure logging drivers
6. Use secrets management for credentials
7. Set up proper networking and reverse proxy

Example production CMD:
```dockerfile
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
```

## Network Configuration

All services are on the default Docker network and can communicate using service names:
- Middleware → Backend: `http://backend:8001`
- Backend → Database: `postgresql+psycopg://app:app@db:5432/app`

## Volumes

- `db_data`: Persistent PostgreSQL data

To backup the database:
```bash
docker-compose exec db pg_dump -U app app > backup.sql
```

To restore:
```bash
docker-compose exec -T db psql -U app app < backup.sql
```
