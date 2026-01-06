# Ubuntu Local Testing Guide for DiscussIt

This guide provides step-by-step instructions for setting up and testing DiscussIt on Ubuntu 22.04 LTS or later. Follow these Ubuntu-specific instructions to get the development environment running smoothly.

## Table of Contents

- [System Requirements](#system-requirements)
- [Backend Setup](#backend-setup)
- [Frontend Setup](#frontend-setup)
- [Database Setup](#database-setup)
- [Running the Application](#running-the-application)
- [Testing API Endpoints](#testing-api-endpoints)
- [Common Issues & Troubleshooting](#common-issues--troubleshooting)
- [Development Workflow](#development-workflow)

## System Requirements

### Minimum Requirements

- **Operating System:** Ubuntu 22.04 LTS or later
- **RAM:** 8GB (16GB recommended for smooth development)
- **Disk Space:** 10GB free space
- **CPU:** Dual-core processor (Quad-core recommended)

### Software Requirements

**Backend:**
- Python 3.12+
- PostgreSQL 15+
- Redis 7+
- pip (Python package manager)

**Frontend:**
- Node.js 18+
- npm 9+

**Optional but Recommended:**
- Docker (for containerized development)
- VS Code (IDE)
- Postman (API testing)
- pgAdmin (PostgreSQL management)

## Backend Setup

### 1. Clone the Repository

```bash
git clone https://github.com/adampzb/discuss.git
cd discuss
```

### 2. Set Up Python Virtual Environment

```bash
cd backend
python3 -m venv venv
```

**Activate the virtual environment:**

- **Linux/macOS:**
```bash
source venv/bin/activate
```

- **Windows (PowerShell):**
```powershell
.\venv\Scripts\Activate.ps1
```

- **Windows (CMD):**
```cmd
venv\Scripts\activate.bat
```

### 3. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file by copying the example:

```bash
cp .env.example .env
```

Edit the `.env` file with your local configuration. Here's a basic configuration:

```env
# Django settings
DJANGO_ENV=development
DJANGO_SECRET_KEY=your-secret-key-here
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1

# Database settings
DB_NAME=discussit
DB_USER=discussit
```

**Important: Generate a proper Django secret key**

For security, never use the example secret key in production or even development. Generate a proper secret key:

```bash
# Method 1: Use Django's built-in secret key generator
cd backend
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

# Method 2: Use openssl (if available)
openssl rand -hex 32

# Method 3: Use Python directly
python -c "import secrets; print(secrets.token_urlsafe(50))"
```

Copy the generated key and replace `your-secret-key-here` in your `.env` file:

```env
DJANGO_SECRET_KEY=your-generated-secret-key-here
```

**Security Note:**
- Keep your secret key private
- Never commit it to version control
- Use different keys for development, staging, and production
- Rotate keys regularly in production environments
DB_PASSWORD=discussit
DB_HOST=localhost
DB_PORT=5432

# Redis settings
REDIS_HOST=localhost
REDIS_PORT=6379

# CORS settings
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000

# Email settings (for development)
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
DEFAULT_FROM_EMAIL=noreply@discussit.eu
```

## Frontend Setup

### 1. Install Node.js Dependencies

```bash
cd ../frontend
npm install
```

### 2. Configure Frontend Environment

Create a `.env` file in the frontend directory:

```bash
touch .env
```

Add the following configuration:

```env
REACT_APP_API_URL=http://localhost:8000/api
REACT_APP_WS_URL=ws://localhost:8000
REACT_APP_ENV=development
```

## Database Setup

### 1. Install PostgreSQL

**Ubuntu:**
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
```

### 2. Create Database and User

```bash
sudo -u postgres psql
```

In the PostgreSQL shell:
```sql
CREATE DATABASE discussit;
CREATE USER discussit WITH PASSWORD 'discussit';
ALTER ROLE discussit SET client_encoding TO 'utf8';
ALTER ROLE discussit SET default_transaction_isolation TO 'read committed';
ALTER ROLE discussit SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE discussit TO discussit;
\q
```

**Note for Ubuntu:** If you get a "peer authentication failed" error, you may need to modify the PostgreSQL configuration:

```bash
sudo nano /etc/postgresql/15/main/pg_hba.conf
```

Find the line:
```
local   all             postgres                                peer
```

And change it to:
```
local   all             postgres                                md5
```

Then restart PostgreSQL:
```bash
sudo systemctl restart postgresql
```

### 3. Run Database Migrations

```bash
cd ../backend
python manage.py migrate
```

### 4. Create Superuser (Optional)

```bash
python manage.py createsuperuser
```

Follow the prompts to create an admin user.

## Running the Application

### 1. Start Redis Server

```bash
# Install Redis if not already installed
sudo apt update
sudo apt install redis-server

# Start Redis service
sudo systemctl start redis
sudo systemctl enable redis

# Verify Redis is running
redis-cli ping  # Should return "PONG"
```

### 2. Start Backend Development Server

```bash
cd backend
python manage.py runserver
```

The backend will be available at `http://localhost:8000`

### 3. Start Frontend Development Server

```bash
cd ../frontend
npm start
```

The frontend will be available at `http://localhost:3000`

### 4. Start Celery Worker (Optional)

```bash
# Install Celery if needed
cd ../backend
pip install celery

# Start Celery worker
celery -A backend worker --loglevel=info
```

## Testing API Endpoints

### Using Postman

1. **Install Postman** from [postman.com](https://www.postman.com/)
2. **Import our API collection** (when available)
3. **Set base URL** to `http://localhost:8000/api`

### Using curl

**Test authentication:**
```bash
# Register a new user
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "testpass123", "name": "Test User"}'

# Login
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "testpass123"}'
```

**Test forum endpoints:**
```bash
# Create a subforum (authenticated)
curl -X POST http://localhost:8000/api/forums/subforums/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{"name": "Technology", "description": "Discuss technology topics", "privacy": "public"}'

# List subforums
curl -X GET http://localhost:8000/api/forums/subforums/
```

## Common Issues & Troubleshooting

### Ubuntu-Specific Issues

**Problem:** `ModuleNotFoundError` when running Django

**Solution:**
```bash
source venv/bin/activate  # Activate virtual environment
pip install -r requirements.txt
```

**Problem:** Database connection errors

**Solution:**
```bash
# Check PostgreSQL service status
sudo systemctl status postgresql

# If not running, start it
sudo systemctl start postgresql

# Verify your .env database settings
cat backend/.env | grep DB_

# Test database connection
sudo -u postgres psql -c "\l"
```

**Problem:** Redis connection errors

**Solution:**
```bash
# Check Redis service status
sudo systemctl status redis

# If not running, start it
sudo systemctl start redis

# Test Redis connection
redis-cli ping  # Should return "PONG"

# Check Redis configuration
cat backend/.env | grep REDIS_
```

**Problem:** `npm` command not found

**Solution:**
```bash
# Install Node.js on Ubuntu
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install -y nodejs

# Verify installation
node -v
npm -v
```

**Problem:** Frontend won't connect to backend

**Solution:**
```bash
# Check CORS settings
cat backend/backend/settings.py | grep CORS_ALLOWED_ORIGINS

# Ensure backend is running
curl -I http://localhost:8000

# Verify frontend API URL
cat frontend/.env | grep REACT_APP_API_URL

# Check firewall settings
sudo ufw status
```

**Problem:** Missing dependencies

**Solution:**
```bash
cd frontend
rm -rf node_modules package-lock.json
npm cache clean --force
npm install
```

**Problem:** Port already in use

**Solution:**
```bash
# Find process using port 8000
sudo lsof -i :8000

# Kill process (replace PID with actual process ID)
sudo kill -9 PID

# Or find and kill all Python processes
pkill -f "python.*manage.py"
```

## Development Workflow

### Typical Development Session

1. **Start services:**
```bash
# Terminal 1: Start Redis service
sudo systemctl start redis
redis-cli ping  # Verify it's running

# Terminal 2: Backend
cd backend
source venv/bin/activate
python manage.py runserver

# Terminal 3: Frontend
cd frontend
npm start

# Terminal 4: Celery (optional)
cd backend
celery -A backend worker --loglevel=info
```

2. **Make changes** to backend or frontend code

3. **Test your changes** using Postman or browser

4. **Run tests:**
```bash
# Backend tests
cd backend
python manage.py test

# Frontend tests
cd frontend
npm test
```

5. **Create migrations** (if you changed models):
```bash
cd backend
python manage.py makemigrations
python manage.py migrate
```

### Debugging Tips

**Backend Debugging:**
- Use Django debug toolbar (install with `pip install django-debug-toolbar`)
- Add `import pdb; pdb.set_trace()` in your code for breakpoints
- Check Django logs for errors

**Frontend Debugging:**
- Use Chrome DevTools (F12)
- Add `console.log()` statements
- Use React Developer Tools browser extension

## Accessing Admin Interface

1. Ensure you have created a superuser (see Database Setup)
2. Start the backend server
3. Visit `http://localhost:8000/admin`
4. Login with your superuser credentials

## Testing Real-time Features

Our real-time features use WebSockets via Django Channels. To test:

1. Ensure Redis is running
2. Start the Django development server (it handles both HTTP and WebSocket)
3. Use the frontend to test real-time updates (comments, notifications, etc.)

## Performance Testing

For local performance testing:

```bash
# Install locust
pip install locust

# Run load tests
locust -f locustfile.py
```

Then visit `http://localhost:8089` to run tests.

## Docker Development (Optional)

If you prefer Docker on Ubuntu:

```bash
# Install Docker on Ubuntu
sudo apt update
sudo apt install -y docker.io docker-compose
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -aG docker $USER
newgrp docker  # Refresh group membership

# Build and start containers
docker-compose up --build

# Run migrations in container
docker-compose exec backend python manage.py migrate

# Create superuser in container
docker-compose exec backend python manage.py createsuperuser

# Stop containers
docker-compose down
```

## Additional Resources

- **Django Documentation:** https://docs.djangoproject.com/
- **React Documentation:** https://react.dev/
- **PostgreSQL Documentation:** https://www.postgresql.org/docs/
- **Redis Documentation:** https://redis.io/docs/

## Support

If you encounter issues not covered in this guide:

- Check our [GitHub Issues](https://github.com/adampzb/discuss/issues)
- Contact the development team via Slack
- Email support@discussit.eu

Happy coding! 🚀