# DiscussIt Backend

## Authentication System

DiscussIt uses a **hybrid authentication architecture** combining django-allauth and custom JWT authentication.

### django-allauth (Web Authentication)

**Purpose:** Traditional web authentication with email verification, password reset, and social login.

**URLs:** `/accounts/`

**Features:**
- Email-based registration and login
- Email verification workflows
- Password reset functionality
- Social authentication (Google, Facebook, etc.)
- Django admin integration

**Configuration:**
```python
# Already configured in settings.py
INSTALLED_APPS = [
    ...
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
]

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]
```

### Custom JWT (API Authentication)

**Purpose:** Stateless authentication for React SPA and mobile applications.

**URLs:** `/api/auth/`

**Endpoints:**
- `POST /api/auth/register/` - Register with email/password
- `POST /api/auth/login/` - Login with email/password
- `POST /api/auth/token/refresh/` - Refresh access token
- `POST /api/auth/logout/` - Logout and blacklist token
- `GET /api/auth/profile/` - Get user profile

**Features:**
- JWT token generation and validation
- Automatic token refresh
- Token blacklisting
- API rate limiting
- Custom user serialization

## Why This Hybrid Approach?

1. **Leverage Django Packages:** Use battle-tested django-allauth instead of reinventing the wheel
2. **Modern SPA Support:** Custom JWT for React frontend needs
3. **Best of Both Worlds:** Web auth for admin, JWT for APIs
4. **Reduced Maintenance:** Less custom code to maintain
5. **Security:** Both systems benefit from Django's security features

## Getting Started

### Prerequisites

- Python 3.12+
- PostgreSQL 12+
- Node.js 18+ (for frontend)

### Installation

```bash
# Clone repository
git clone https://github.com/adampzb/discussit.git
cd discussit/backend

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your database credentials

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Start development server
python manage.py runserver
```

### Configuration

**Database:** PostgreSQL (recommended)

**Email:** Configure in `.env`
```env
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.yourprovider.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your@email.com
EMAIL_HOST_PASSWORD=yourpassword
DEFAULT_FROM_EMAIL=noreply@discussit.eu
```

**CORS:** Configure allowed origins
```python
# settings.py
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5174",  # Frontend dev server
    "https://yourdomain.com",  # Production frontend
]
```

## Development

### Running Tests

```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test users

# Check code quality
python -m flake8
python -m black --check .
python -m isort --check .
```

### API Documentation

**Base URL:** `http://localhost:8000/api/`

**Authentication Endpoints:**
- `POST /auth/register/` - User registration
- `POST /auth/login/` - User login
- `POST /auth/token/refresh/` - Token refresh
- `POST /auth/logout/` - User logout
- `GET /auth/profile/` - User profile

**Example Request:**
```bash
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"securepassword","first_name":"John","last_name":"Doe"}'
```

**Example Response:**
```json
{
  "user": {
    "id": 1,
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Doe"
  },
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

## Deployment

### Production Checklist

- [ ] Set `DEBUG=False`
- [ ] Configure proper email backend
- [ ] Set up HTTPS
- [ ] Configure CORS origins
- [ ] Set secure cookie settings
- [ ] Configure logging
- [ ] Set up monitoring
- [ ] Configure backups

### Docker Deployment

```bash
# Build Docker image
docker build -t discussit-backend .

# Run container
docker run -p 8000:8000 \
  -e DATABASE_URL=postgres://user:password@db:5432/discussit \
  -e SECRET_KEY=your-secret-key \
  discussit-backend
```

## Architecture

### Key Components

1. **django-allauth:** Web authentication
2. **Django REST Framework:** API framework
3. **SimpleJWT:** JWT authentication
4. **PostgreSQL:** Database
5. **CORS Headers:** Cross-origin resource sharing
6. **Security Middleware:** Enhanced security headers

### Security Features

- ✅ Content Security Policy
- ✅ Permissions Policy
- ✅ XSS Protection
- ✅ Referrer Policy
- ✅ HSTS
- ✅ Rate Limiting
- ✅ CSRF Protection
- ✅ JWT Token Security

## Contributing

### Code Quality

```bash
# Format code
python -m black .
python -m isort .

# Lint code
python -m flake8

# Type checking (if using)
mypy .
```

### Commit Guidelines

- Use conventional commits
- Keep commits small and focused
- Write descriptive commit messages
- Include related issue numbers

## License

MIT License - See LICENSE file for details.

## Support

For questions or issues:
- Check the documentation
- Review the architecture guide
- Consult Django and allauth documentation
- Open an issue on GitHub

## Roadmap

### Future Enhancements

- Social authentication providers
- Two-factor authentication
- Advanced rate limiting
- API versioning
- OpenAPI/Swagger documentation
- WebSocket authentication

## Documentation

- [Authentication Architecture](AUTHENTICATION_ARCHITECTURE.md)
- [API Specification](../API_SPECIFICATION.md)
- [Django Documentation](https://docs.djangoproject.com/)
- [django-allauth Documentation](https://django-allauth.readthedocs.io/)
- [Django REST Framework](https://www.django-rest-framework.org/)

## Contact

For project-related questions, please use GitHub issues.
