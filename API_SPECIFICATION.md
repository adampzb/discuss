# DiscussIt API Specification

**Version:** 1.0
**Last Updated:** 2024
**Base URL:** `/api/`

## Table of Contents

1. [Authentication](#authentication)
2. [User Management](#user-management)
3. [Profile Management](#profile-management)
4. [Social Features](#social-features)
5. [Admin Management](#admin-management)
6. [Error Responses](#error-responses)
7. [Authentication](#authentication-1)

## Authentication

All API endpoints require authentication using JWT (JSON Web Tokens).

### Authentication Flow

1. **Obtain Token**: `POST /api/auth/login/`
2. **Use Token**: Include in `Authorization: Bearer <token>` header
3. **Refresh Token**: `POST /api/auth/token/refresh/`
4. **Logout**: `POST /api/auth/logout/`

### Token Structure

```json
{
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "is_staff": false,
    "is_active": true
  }
}
```

### Token Lifecycle

- **Access Token**: Valid for 60 minutes
- **Refresh Token**: Valid for 1 day
- **Token Rotation**: Refresh tokens are rotated on use
- **Blacklisting**: Tokens can be blacklisted on logout

## User Management

### 1. User Registration

**Endpoint:** `POST /api/auth/register/`

**Description:** Register a new user

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "securePassword123!",
  "password_confirmation": "securePassword123!",
  "first_name": "John",
  "last_name": "Doe",
  "bio": "Software developer",
  "date_of_birth": "1990-01-01"
}
```

**Response (201 Created):**
```json
{
  "user": {
    "id": 1,
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "bio": "Software developer",
    "date_of_birth": "1990-01-01",
    "is_active": true,
    "is_staff": false
  },
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Error Responses:**
- `400 Bad Request`: Invalid data, passwords don't match, weak password
- `409 Conflict`: Email already exists

### 2. User Login

**Endpoint:** `POST /api/auth/login/`

**Description:** Authenticate user and obtain JWT tokens

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "securePassword123!"
}
```

**Response (200 OK):**
```json
{
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "is_staff": false,
    "is_active": true
  }
}
```

**Error Responses:**
- `401 Unauthorized`: Invalid credentials
- `403 Forbidden`: Account inactive
- `429 Too Many Requests`: Rate limited (5 attempts per hour)

### 3. Token Refresh

**Endpoint:** `POST /api/auth/token/refresh/`

**Description:** Obtain new access token using refresh token

**Request Body:**
```json
{
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Response (200 OK):**
```json
{
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Error Responses:**
- `401 Unauthorized`: Invalid or expired refresh token
- `400 Bad Request`: Malformed request

### 4. Password Reset Request

**Endpoint:** `POST /api/auth/password-reset/`

**Description:** Request password reset email

**Request Body:**
```json
{
  "email": "user@example.com"
}
```

**Response (200 OK):**
```json
{
  "detail": "If a user with this email exists, a password reset link has been sent."
}
```

**Error Responses:**
- `400 Bad Request`: Invalid email format

### 5. Password Reset Confirmation

**Endpoint:** `POST /api/auth/password-reset/<uidb64>/<token>/`

**Description:** Reset password using token from email

**Request Body:**
```json
{
  "password": "newSecurePassword123!",
  "password_confirmation": "newSecurePassword123!"
}
```

**Response (200 OK):**
```json
{
  "detail": "Password has been reset successfully."
}
```

**Error Responses:**
- `400 Bad Request`: Invalid token, passwords don't match, weak password
- `404 Not Found`: User not found

### 6. User Logout

**Endpoint:** `POST /api/auth/logout/`

**Description:** Invalidate refresh token (logout)

**Headers:**
```
Authorization: Bearer <access_token>
```

**Request Body:**
```json
{
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Response (200 OK):**
```json
{
  "detail": "Successfully logged out."
}
```

**Error Responses:**
- `400 Bad Request`: Invalid token
- `401 Unauthorized`: Not authenticated

### 7. User Profile

**Endpoint:** `GET /api/auth/profile/`

**Description:** Get current user profile

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response (200 OK):**
```json
{
  "id": 1,
  "email": "user@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "bio": "Software developer",
  "profile_picture": null,
  "date_of_birth": "1990-01-01",
  "is_active": true,
  "is_staff": false
}
```

**Error Responses:**
- `401 Unauthorized`: Not authenticated

### 8. Update User Profile

**Endpoint:** `PUT /api/auth/profile/`

**Description:** Update current user profile

**Headers:**
```
Authorization: Bearer <access_token>
```

**Request Body:**
```json
{
  "first_name": "John",
  "last_name": "Doe",
  "bio": "Senior Software Developer",
  "date_of_birth": "1990-01-01",
  "password": "newPassword123!",
  "password_confirmation": "newPassword123!"
}
```

**Response (200 OK):**
```json
{
  "id": 1,
  "email": "user@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "bio": "Senior Software Developer",
  "profile_picture": null,
  "date_of_birth": "1990-01-01",
  "is_active": true,
  "is_staff": false
}
```

**Error Responses:**
- `400 Bad Request`: Invalid data, passwords don't match
- `401 Unauthorized`: Not authenticated

## Profile Management

### 1. Get User Profile (Extended)

**Endpoint:** `GET /api/auth/profiles/profile/`

**Description:** Get extended user profile with social information

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response (200 OK):**
```json
{
  "id": 1,
  "email": "user@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "bio": "Software developer",
  "profile_picture": null,
  "date_of_birth": "1990-01-01",
  "privacy_setting": "public",
  "email_notifications": true,
  "push_notifications": true,
  "website": "https://example.com",
  "github_username": "johndoe",
  "twitter_username": "johndoe",
  "linkedin_username": "johndoe",
  "location": "San Francisco, CA",
  "occupation": "Software Developer",
  "company": "Tech Corp",
  "theme_preference": "system",
  "language_preference": "en",
  "profile_background": null,
  "followers_count": 42,
  "following_count": 15,
  "last_active": "2024-02-20T12:00:00Z",
  "date_created": "2024-02-01T10:00:00Z"
}
```

**Error Responses:**
- `401 Unauthorized`: Not authenticated
- `403 Forbidden`: Trying to access private profile without permission

### 2. Get Other User Profile

**Endpoint:** `GET /api/auth/profiles/profile/<user_id>/`

**Description:** Get another user's profile (respects privacy settings)

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response (200 OK):** Same as extended profile, but filtered based on privacy settings

**Error Responses:**
- `401 Unauthorized`: Not authenticated
- `403 Forbidden`: Profile is private and you don't have access
- `404 Not Found`: User not found

### 3. Update Extended Profile

**Endpoint:** `PUT /api/auth/profiles/profile/`

**Description:** Update extended profile information

**Headers:**
```
Authorization: Bearer <access_token>
```

**Request Body:**
```json
{
  "first_name": "John",
  "last_name": "Doe",
  "bio": "Senior Software Developer",
  "website": "https://johndoe.dev",
  "github_username": "johndoe",
  "privacy_setting": "friends",
  "email_notifications": false,
  "theme_preference": "dark"
}
```

**Response (200 OK):** Updated profile object

**Error Responses:**
- `400 Bad Request`: Invalid data
- `401 Unauthorized`: Not authenticated

### 4. Follow User

**Endpoint:** `POST /api/auth/profiles/follow/`

**Description:** Follow or unfollow a user

**Headers:**
```
Authorization: Bearer <access_token>
```

**Request Body:**
```json
{
  "user_id": 2,
  "action": "follow"  // or "unfollow"
}
```

**Response (200 OK):**
```json
{
  "detail": "You are now following user@example.com."
}
```

**Error Responses:**
- `400 Bad Request`: Invalid action
- `401 Unauthorized`: Not authenticated
- `404 Not Found`: User not found

### 5. Block User

**Endpoint:** `POST /api/auth/profiles/block/`

**Description:** Block or unblock a user

**Headers:**
```
Authorization: Bearer <access_token>
```

**Request Body:**
```json
{
  "user_id": 3,
  "action": "block"  // or "unblock"
}
```

**Response (200 OK):**
```json
{
  "detail": "You have blocked user@example.com."
}
```

**Error Responses:**
- `400 Bad Request`: Invalid action
- `401 Unauthorized`: Not authenticated
- `404 Not Found`: User not found

### 6. Search Users

**Endpoint:** `GET /api/auth/profiles/search/?q=<query>`

**Description:** Search for users by email, first name, or last name

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response (200 OK):**
```json
[
  {
    "id": 2,
    "email": "jane@example.com",
    "first_name": "Jane",
    "last_name": "Smith",
    "profile_picture": "https://example.com/profile.jpg",
    "is_following": false
  },
  {
    "id": 3,
    "email": "john.smith@example.com",
    "first_name": "John",
    "last_name": "Smith",
    "profile_picture": null,
    "is_following": true
  }
]
```

**Error Responses:**
- `401 Unauthorized`: Not authenticated

## Admin Management

### 1. List Users

**Endpoint:** `GET /api/auth/management/users/`

**Description:** List all users (admin only)

**Headers:**
```
Authorization: Bearer <access_token>
```

**Query Parameters:**
- `page`: Page number (default: 1)
- `page_size`: Items per page (default: 20, max: 100)
- `search`: Search term for email, first name, last name
- `is_active`: Filter by active status
- `is_staff`: Filter by staff status
- `is_superuser`: Filter by superuser status
- `ordering`: Field to order by (id, email, first_name, last_name, date_joined, last_login)

**Response (200 OK):**
```json
{
  "count": 100,
  "next": "http://api.example.com/api/auth/management/users/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "email": "user@example.com",
      "first_name": "John",
      "last_name": "Doe",
      "is_active": true,
      "is_staff": false,
      "is_superuser": false,
      "date_joined": "2024-01-01T10:00:00Z",
      "last_login": "2024-02-20T12:00:00Z"
    }
  ]
}
```

**Error Responses:**
- `401 Unauthorized`: Not authenticated
- `403 Forbidden`: Not admin user

### 2. Get User Details

**Endpoint:** `GET /api/auth/management/users/<id>/`

**Description:** Get detailed user information (admin only)

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response (200 OK):**
```json
{
  "id": 1,
  "email": "user@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "bio": "Software developer",
  "date_of_birth": "1990-01-01",
  "is_active": true,
  "is_staff": false,
  "is_superuser": false,
  "date_joined": "2024-01-01T10:00:00Z",
  "last_login": "2024-02-20T12:00:00Z"
}
```

**Error Responses:**
- `401 Unauthorized`: Not authenticated
- `403 Forbidden`: Not admin user
- `404 Not Found`: User not found

### 3. Update User

**Endpoint:** `PUT /api/auth/management/users/<id>/`

**Description:** Update user information (admin only)

**Headers:**
```
Authorization: Bearer <access_token>
```

**Request Body:**
```json
{
  "email": "newemail@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "is_active": true,
  "is_staff": true
}
```

**Response (200 OK):** Updated user object

**Error Responses:**
- `400 Bad Request`: Invalid data
- `401 Unauthorized`: Not authenticated
- `403 Forbidden`: Not admin user
- `404 Not Found`: User not found

### 4. Activate/Deactivate User

**Endpoint:** `POST /api/auth/management/users/<id>/activate/`

**Description:** Activate, deactivate, or toggle user status (admin only)

**Headers:**
```
Authorization: Bearer <access_token>
```

**Request Body:**
```json
{
  "action": "activate"  // "deactivate" or "toggle"
}
```

**Response (200 OK):**
```json
{
  "detail": "User user@example.com has been activated."
}
```

**Error Responses:**
- `400 Bad Request`: Invalid action
- `401 Unauthorized`: Not authenticated
- `403 Forbidden`: Not admin user
- `404 Not Found`: User not found

### 5. Delete User

**Endpoint:** `DELETE /api/auth/management/users/<id>/`

**Description:** Delete a user (admin only)

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response (204 No Content):** Empty response

**Error Responses:**
- `401 Unauthorized`: Not authenticated
- `403 Forbidden`: Not admin user
- `404 Not Found`: User not found

### 6. User Statistics

**Endpoint:** `GET /api/auth/management/users/stats/`

**Description:** Get user statistics (admin only)

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response (200 OK):**
```json
{
  "total_users": 100,
  "active_users": 95,
  "inactive_users": 5,
  "staff_users": 3,
  "superusers": 1,
  "recent_users": [
    {
      "id": 1,
      "email": "user@example.com",
      "first_name": "John",
      "last_name": "Doe",
      "date_joined": "2024-02-20T12:00:00Z"
    }
  ]
}
```

**Error Responses:**
- `401 Unauthorized`: Not authenticated
- `403 Forbidden`: Not admin user

### 7. Export User Data

**Endpoint:** `GET /api/auth/management/users/export/`

**Description:** Export user data (admin only)

**Headers:**
```
Authorization: Bearer <access_token>
```

**Query Parameters:**
- `is_active`: Filter by active status
- `is_staff`: Filter by staff status

**Response (200 OK):**
```json
{
  "count": 50,
  "data": [
    {
      "id": 1,
      "email": "user@example.com",
      "first_name": "John",
      "last_name": "Doe",
      "is_active": true,
      "is_staff": false,
      "is_superuser": false,
      "date_joined": "2024-01-01T10:00:00Z",
      "last_login": "2024-02-20T12:00:00Z"
    }
  ]
}
```

**Error Responses:**
- `401 Unauthorized`: Not authenticated
- `403 Forbidden`: Not admin user

## Error Responses

### Standard Error Format

```json
{
  "detail": "Error message",
  "field_errors": {
    "field_name": ["Error message 1", "Error message 2"]
  }
}
```

### Common Error Codes

| Status Code | Error Type | Description |
|-------------|------------|-------------|
| 400 | Bad Request | Invalid request data |
| 401 | Unauthorized | Authentication required |
| 403 | Forbidden | Insufficient permissions |
| 404 | Not Found | Resource not found |
| 409 | Conflict | Resource already exists |
| 429 | Too Many Requests | Rate limit exceeded |
| 500 | Internal Server Error | Server error |

### Example Error Responses

**400 Bad Request:**
```json
{
  "detail": "Invalid data",
  "field_errors": {
    "email": ["This field is required."],
    "password": ["Passwords do not match."]
  }
}
```

**401 Unauthorized:**
```json
{
  "detail": "Authentication credentials were not provided."
}
```

**403 Forbidden:**
```json
{
  "detail": "You do not have permission to perform this action."
}
```

**404 Not Found:**
```json
{
  "detail": "User not found."
}
```

**429 Too Many Requests:**
```json
{
  "detail": "Too many login attempts. Please try again later."
}
```

## Authentication

### JWT Authentication

All endpoints except registration, login, and password reset require JWT authentication.

**Request Header:**
```
Authorization: Bearer <access_token>
```

### Token Management

- **Access Token**: Short-lived (60 minutes), used for API requests
- **Refresh Token**: Long-lived (1 day), used to obtain new access tokens
- **Token Rotation**: Refresh tokens are rotated on each use
- **Blacklisting**: Tokens can be blacklisted on logout

### Rate Limiting

- **Login Attempts**: 5 attempts per hour per IP
- **Password Reset**: 3 attempts per hour per email
- **API Requests**: 100 requests per minute per user

## Versioning

The API uses semantic versioning in the URL:

- Current version: `/api/v1/` (implied, not in URL)
- Future versions: `/api/v2/`

## Pagination

Endpoints that return lists use cursor-based pagination:

```json
{
  "count": 100,
  "next": "http://api.example.com/endpoint/?cursor=cD0yMDI0LTAxLTA2KzAzJTNBMjQlMkIwMCUzQTAw",
  "previous": "http://api.example.com/endpoint/?cursor=cj0x",
  "results": [...]
}
```

## Filtering and Search

Many endpoints support filtering and search:

- `?search=<term>`: Full-text search
- `?field=<value>`: Exact match filtering
- `?field__contains=<term>`: Partial match
- `?ordering=<field>`: Sorting (prefix with `-` for descending)

## Content Types

- **Request**: `application/json`
- **Response**: `application/json`
- **File Uploads**: `multipart/form-data`

## Date and Time Format

All dates and times use ISO 8601 format:

```
YYYY-MM-DDTHH:MM:SSZ  (UTC)
YYYY-MM-DDTHH:MM:SS+HH:MM  (with timezone)
```

## Character Encoding

- **Encoding**: UTF-8
- **Content-Type**: `application/json; charset=utf-8`

## CORS

- **Allowed Origins**: Configured in settings
- **Allowed Methods**: GET, POST, PUT, PATCH, DELETE, OPTIONS
- **Allowed Headers**: Authorization, Content-Type, X-CSRFToken
- **Credentials**: Allowed

## Security

- **HTTPS**: Required in production
- **CORS**: Properly configured
- **CSRF**: Protected for session-based auth
- **Rate Limiting**: Applied to sensitive endpoints
- **Input Validation**: All inputs are validated
- **Password Hashing**: PBKDF2 with SHA256

## Deprecation Policy

- Deprecated endpoints will be marked in responses
- Deprecated endpoints will be supported for at least 6 months
- Deprecation warnings will be included in changelog

## Changelog

### Version 1.0 (Current)
- Initial API specification
- Core authentication endpoints
- User management endpoints
- Profile management endpoints
- Admin management endpoints

## Contact

For API-related questions, please contact:
- **Email**: api-support@discussit.eu
- **GitHub**: github.com/adampzb/discuss
- **Documentation**: docs.discussit.eu

## License

This API specification is licensed under the MIT License. See the LICENSE file for details.