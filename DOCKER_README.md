# DiscussIt Docker Development Environment

This guide explains how to set up and use the Docker development environment for the DiscussIt platform.

## Prerequisites

- Docker (version 20.10+ recommended)
- Docker Compose (version 1.29+ recommended)
- At least 4GB RAM allocated to Docker
- Ports 3000 (frontend), 8000 (backend), 5432 (PostgreSQL), and 6379 (Redis) available

## Quick Start

```bash
# Build and start all services
docker-compose up --build

# Access the application:
# - Frontend: http://localhost:3000
# - Backend: http://localhost:8000
# - Admin: http://localhost:8000/admin
```

## Services

The docker-compose.yml file defines the following services:

### 1. PostgreSQL Database
- **Container**: `discussit_db`
- **Port**: 5432
- **Credentials**: discussit/discussit
- **Volume**: `postgres_data` (persistent storage)

### 2. Redis
- **Container**: `discussit_redis`
- **Port**: 6379
- **Volume**: `redis_data` (persistent storage)

### 3. Django Backend
- **Container**: `discussit_backend`
- **Port**: 8000
- **Volumes**: 
  - `backend_static` (static files)
  - `backend_media` (media uploads)
- **Environment Variables**: Configured in docker-compose.yml

### 4. React Frontend
- **Container**: `discussit_frontend`
- **Port**: 3000
- **Volume**: `frontend_node_modules` (node modules cache)

### 5. Celery Worker
- **Container**: `discussit_celery`
- **Purpose**: Async task processing

### 6. Celery Beat
- **Container**: `discussit_celery_beat`
- **Purpose**: Scheduled task processing

## Common Commands

### Start the development environment
```bash
docker-compose up --build
```

### Start in detached mode
```bash
docker-compose up --build -d
```

### Stop all services
```bash
docker-compose down
```

### Stop and remove volumes (clean slate)
```bash
docker-compose down -v
```

### View logs
```bash
docker-compose logs
# For a specific service
docker-compose logs backend
```

### Run management commands
```bash
# Access the backend container
docker-compose exec backend sh

# Then run Django commands
python manage.py createsuperuser
python manage.py makemigrations
python manage.py migrate
```

### Run tests
```bash
docker-compose exec backend python manage.py test
```

## Environment Variables

The backend service uses the following environment variables (configured in docker-compose.yml):

- `DJANGO_ENV`: development
- `DJANGO_SECRET_KEY`: Development secret key
- `DB_NAME`: discussit
- `DB_USER`: discussit
- `DB_PASSWORD`: discussit
- `DB_HOST`: db (Docker service name)
- `DB_PORT`: 5432
- `CORS_ALLOWED_ORIGINS`: Frontend URLs

## Development Workflow

### 1. Backend Development

1. Make changes to files in the `backend/` directory
2. Changes are automatically reflected in the container due to volume mounting
3. The backend will auto-reload when Python files change

### 2. Frontend Development

1. Make changes to files in the `frontend/` directory
2. Changes are automatically reflected in the container
3. The frontend will hot-reload when files change

### 3. Database Management

- Data is persisted in the `postgres_data` volume
- To reset the database: `docker-compose down -v` then `docker-compose up --build`

## Troubleshooting

### Port conflicts
If you get port conflicts, you can:
1. Stop other services using those ports
2. Modify the port mappings in docker-compose.yml
3. Use `docker-compose down` to clean up

### Database connection issues
1. Ensure PostgreSQL container is healthy: `docker-compose ps`
2. Check logs: `docker-compose logs db`
3. Try restarting: `docker-compose restart db`

### Dependency issues
1. Rebuild containers: `docker-compose build --no-cache`
2. Clear Python cache: `docker-compose exec backend rm -rf __pycache__`
3. Reinstall dependencies: `docker-compose exec backend pip install -r requirements.txt`

## Production Considerations

This Docker setup is optimized for **development**. For production, you should:

1. Use proper secret management (not hardcoded secrets)
2. Configure proper security settings
3. Use a production-ready web server (Gunicorn + Nginx)
4. Set up proper logging and monitoring
5. Configure proper database backups
6. Use HTTPS with proper certificates

## Networking

All services are connected via a custom Docker network (`discussit_network`). Services can communicate using their container names as hostnames:

- `db` for PostgreSQL
- `redis` for Redis
- `backend` for Django backend
- `frontend` for React frontend

## Volumes

The following volumes are used for persistent data:

- `postgres_data`: PostgreSQL database files
- `redis_data`: Redis data
- `backend_static`: Django static files
- `backend_media`: Django media uploads
- `frontend_node_modules`: Node.js dependencies

To clean up all volumes:
```bash
docker-compose down -v
```

## Updating Dependencies

### Backend (Python)
1. Update `backend/requirements.txt`
2. Rebuild the container: `docker-compose build backend`
3. Restart: `docker-compose up -d`

### Frontend (Node.js)
1. Update `frontend/package.json`
2. Rebuild the container: `docker-compose build frontend`
3. Restart: `docker-compose up -d`

## Useful Tips

### Access PostgreSQL directly
```bash
docker-compose exec db psql -U discussit -d discussit
```

### Access Redis directly
```bash
docker-compose exec redis redis-cli
```

### Shell into backend container
```bash
docker-compose exec backend sh
```

### Shell into frontend container
```bash
docker-compose exec frontend sh
```

## Performance Optimization

For better performance during development:

1. **Increase Docker resources**: Allocate more RAM and CPU to Docker
2. **Use bind mounts**: Already configured for instant file changes
3. **Cache dependencies**: Node modules are cached in a volume
4. **Use smaller base images**: Alpine-based images are already used

## Security Notes

- Never commit secrets in Dockerfiles or docker-compose.yml for production
- Use Docker secrets or environment files for sensitive data
- Keep Docker images updated with security patches
- Scan images for vulnerabilities regularly