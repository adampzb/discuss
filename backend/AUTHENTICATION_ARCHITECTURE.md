# DiscussIt Authentication Architecture

## Overview

DiscussIt uses a **hybrid authentication system** that combines the best of both worlds:

1. **django-allauth** for traditional web authentication (session-based)
2. **Custom JWT authentication** for API/SPA authentication (token-based)

## Why This Approach?

### django-allauth Benefits
- **Battle-tested** authentication system
- **Built-in features**: email verification, password reset, social auth
- **Django admin integration**
- **Security best practices** built-in
- **Reduces custom code** maintenance

### Custom JWT Benefits
- **Stateless authentication** for SPAs
- **Token-based** for React frontend
- **Automatic token refresh**
- **Fine-grained API control**

## Architecture Components

### 1. django-allauth Configuration

**URLs:** `/accounts/` (allauth default routes)

**Features:**
- User registration with email verification
- Password reset functionality
- Email confirmation workflows
- Social authentication (Google, Facebook, etc.)
- Admin interface integration

**Configuration:**
```python
# backend/settings.py
INSTALLED_APPS = [
    ...
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    ...
]

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",  # Default
    "allauth.account.auth_backends.AuthenticationBackend",  # allauth
]

# Allauth settings
ACCOUNT_USER_MODEL_USERNAME_FIELD = None  # Use email instead of username
ACCOUNT_EMAIL_VERIFICATION = "mandatory"  # Require email verification
ACCOUNT_AUTHENTICATION_METHOD = "email"  # Login with email only
```

### 2. Custom JWT API Authentication

**URLs:** `/api/auth/` (custom API endpoints)

**Endpoints:**
- `POST /api/auth/register/` - User registration (returns JWT tokens)
- `POST /api/auth/login/` - User login (returns JWT tokens)
- `POST /api/auth/token/refresh/` - Token refresh
- `POST /api/auth/logout/` - Logout (blacklists refresh token)
- `GET /api/auth/profile/` - Get user profile

**Features:**
- JWT token generation and validation
- Automatic token refresh with interceptors
- Token blacklisting on logout
- Custom user serialization
- API rate limiting

**Configuration:**
```python
# backend/settings.py
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=30),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
}
```

## When to Use Each System

### Use django-allauth for:
- **Admin interface** authentication
- **Traditional web pages** (if any)
- **Email verification** workflows
- **Password reset** functionality
- **Social authentication** (Google, Facebook, etc.)

### Use Custom JWT for:
- **React SPA authentication**
- **Mobile app authentication**
- **API-only endpoints**
- **Stateless authentication** needs
- **Single Page Applications**

## Frontend Integration

The React frontend uses the **custom JWT API** for authentication:

```typescript
// frontend/src/services/api.ts
const api = axios.create({
  baseURL: 'http://localhost:8000/api/auth',
  headers: {
    'Content-Type': 'application/json',
  },
});

// Automatic token injection
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('accessToken');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Automatic token refresh
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    if (error.response?.status === 401) {
      // Attempt token refresh
      const refreshToken = localStorage.getItem('refreshToken');
      const response = await axios.post('/api/auth/token/refresh/', { refresh: refreshToken });
      localStorage.setItem('accessToken', response.data.access);
      error.config.headers.Authorization = `Bearer ${response.data.access}`;
      return api(error.config);
    }
    return Promise.reject(error);
  }
);
```

## Security Considerations

### django-allauth Security:
- ✅ CSRF protection built-in
- ✅ Session security
- ✅ Password hashing
- ✅ Rate limiting
- ✅ Email verification

### JWT Security:
- ✅ Token expiration (30 min access, 1 day refresh)
- ✅ Token refresh rotation
- ✅ Refresh token blacklisting
- ✅ HTTPS required
- ✅ Secure token storage
- ✅ Content Security Policy headers

### Combined Security:
- ✅ Both systems use the same User model
- ✅ Password hashing is consistent
- ✅ Email verification applies to both
- ✅ Rate limiting protects both
- ✅ Security headers apply to all responses

## Database Schema

Both systems use the same `users.User` model:

```python
# backend/users/models.py
class User(AbstractUser):
    username = None  # Use email as username
    email = models.EmailField(unique=True)
    
    # Custom fields
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
```

## Deployment Considerations

### Development:
- ✅ Console email backend (prints to console)
- ✅ Debug mode enabled
- ✅ CORS allowed for frontend

### Production:
- ✅ Use real email backend (SMTP, SendGrid, etc.)
- ✅ Disable debug mode
- ✅ Set proper CORS origins
- ✅ Configure HTTPS
- ✅ Set secure cookie flags
- ✅ Enable rate limiting

## Migration Path

If you need to migrate from custom JWT to allauth (or vice versa):

1. **Keep both systems running** during transition
2. **Update frontend gradually** to use new endpoints
3. **Maintain backward compatibility** during transition
4. **Test thoroughly** before full switch

## Best Practices

1. **Use django-allauth for:** Admin, email workflows, social auth
2. **Use JWT for:** SPA authentication, mobile apps, APIs
3. **Keep security headers** consistent across both
4. **Use same User model** for both systems
5. **Document clearly** which system to use when
6. **Test both systems** regularly

## Troubleshooting

### Common Issues:

**Issue:** "Email not sent"
- **Solution:** Check email backend configuration
- **Solution:** Verify SMTP settings in production

**Issue:** "Invalid token"
- **Solution:** Check token expiration
- **Solution:** Verify token storage in frontend

**Issue:** "CSRF verification failed"
- **Solution:** Ensure CSRF token is included in forms
- **Solution:** Use `@csrf_exempt` for API endpoints

**Issue:** "User already exists"
- **Solution:** Check email uniqueness
- **Solution:** Implement proper error handling

## Conclusion

This hybrid approach gives DiscussIt the best of both worlds:
- **django-allauth** for robust, feature-rich web authentication
- **Custom JWT** for modern SPA/mobile authentication

Both systems work together seamlessly, sharing the same user database and security policies while providing the right authentication method for each use case.

## References

- [django-allauth documentation](https://django-allauth.readthedocs.io/)
- [Django REST Framework JWT](https://django-rest-framework-simplejwt.readthedocs.io/)
- [Django authentication](https://docs.djangoproject.com/en/stable/topics/auth/)
- [JWT.io](https://jwt.io/)
