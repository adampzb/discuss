from django.utils.deprecation import MiddlewareMixin
from django.conf import settings
from django.http import JsonResponse
from django.utils import timezone
from .models import UserSession
import logging

logger = logging.getLogger(__name__)


class SecurityHeadersMiddleware(MiddlewareMixin):
    """
    Add security headers to all responses.
    """
    
    def process_response(self, request, response):
        # Add security headers
        response['X-Content-Type-Options'] = 'nosniff'
        response['X-Frame-Options'] = 'DENY'
        response['X-XSS-Protection'] = '1; mode=block'
        response['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        response['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains; preload'
        response['Content-Security-Policy'] = """
            default-src 'self';
            script-src 'self' 'unsafe-inline' 'unsafe-eval';
            style-src 'self' 'unsafe-inline';
            img-src 'self' data:;
            font-src 'self';
            connect-src 'self';
            frame-src 'none';
            object-src 'none';
            base-uri 'self';
            form-action 'self';
        """
        response['Permissions-Policy'] = """
            geolocation=(),
            microphone=(),
            camera=(),
            payment=(),
            usb=()
        """
        
        return response


class SessionSecurityMiddleware(MiddlewareMixin):
    """
    Enhance session security and track user sessions.
    """
    
    def process_request(self, request):
        # Skip for API endpoints that don't require session
        if getattr(request, '_dont_enforce_csrf_checks', False):
            return
        
        # Track user sessions
        if request.user.is_authenticated:
            self._track_user_session(request)
            self._check_session_validity(request)
    
    def _track_user_session(self, request):
        """Track user session activity."""
        try:
            session_key = request.session.session_key
            if session_key:
                UserSession.objects.update_or_create(
                    session_key=session_key,
                    defaults={
                        'user': request.user,
                        'last_activity': timezone.now(),
                        'is_active': True
                    }
                )
        except Exception as e:
            logger.error(f"Error tracking user session: {e}")
    
    def _check_session_validity(self, request):
        """Check if session is valid and not hijacked."""
        try:
            session_key = request.session.session_key
            if session_key:
                # Check if this session belongs to the current user
                session = UserSession.objects.get(session_key=session_key)
                if session.user != request.user:
                    logger.warning(f"Potential session hijacking detected for user {request.user.email}")
                    # Invalidate the session
                    request.session.flush()
                    return JsonResponse(
                        {'error': 'Session invalid. Please login again.'},
                        status=403
                    )
        except UserSession.DoesNotExist:
            pass
        except Exception as e:
            logger.error(f"Error checking session validity: {e}")


class RateLimitMiddleware(MiddlewareMixin):
    """
    Simple rate limiting middleware for sensitive endpoints.
    """
    
    RATE_LIMITS = {
        'login': {'limit': 5, 'period': 3600},  # 5 attempts per hour
        'register': {'limit': 10, 'period': 86400},  # 10 attempts per day
        'password_reset': {'limit': 3, 'period': 3600},  # 3 attempts per hour
    }
    
    def __init__(self, get_response):
        super().__init__(get_response)
        self.cache = {}
    
    def process_request(self, request):
        # Check if this is a rate-limited endpoint
        endpoint = self._get_endpoint_name(request)
        
        if endpoint in self.RATE_LIMITS:
            limit_data = self.RATE_LIMITS[endpoint]
            
            # Get client identifier (IP for now, could use user ID if authenticated)
            client_id = self._get_client_identifier(request)
            cache_key = f"rate_limit:{endpoint}:{client_id}"
            
            # Check rate limit
            if self._is_rate_limited(cache_key, limit_data):
                return JsonResponse(
                    {'error': f'Too many requests. Please try again later.'},
                    status=429
                )
            else:
                self._increment_request_count(cache_key)
    
    def _get_endpoint_name(self, request):
        """Get endpoint name from path."""
        path = request.path
        if '/api/auth/login/' in path:
            return 'login'
        elif '/api/auth/register/' in path:
            return 'register'
        elif '/api/auth/password-reset/' in path:
            return 'password_reset'
        return None
    
    def _get_client_identifier(self, request):
        """Get client identifier for rate limiting."""
        if request.user.is_authenticated:
            return f"user:{request.user.id}"
        else:
            return f"ip:{request.META.get('REMOTE_ADDR', 'unknown')}"
    
    def _is_rate_limited(self, cache_key, limit_data):
        """Check if client has exceeded rate limit."""
        if cache_key not in self.cache:
            self.cache[cache_key] = {'count': 0, 'timestamp': timezone.now()}
            return False
        
        # Reset count if period has passed
        if (timezone.now() - self.cache[cache_key]['timestamp']).seconds > limit_data['period']:
            self.cache[cache_key] = {'count': 0, 'timestamp': timezone.now()}
            return False
        
        # Check if limit exceeded
        return self.cache[cache_key]['count'] >= limit_data['limit']
    
    def _increment_request_count(self, cache_key):
        """Increment request count for client."""
        if cache_key in self.cache:
            self.cache[cache_key]['count'] += 1
        else:
            self.cache[cache_key] = {'count': 1, 'timestamp': timezone.now()}


class SecurityLoggingMiddleware(MiddlewareMixin):
    """
    Log security-related events.
    """
    
    def process_request(self, request):
        # Log suspicious requests
        if self._is_suspicious_request(request):
            self._log_suspicious_request(request)
    
    def _is_suspicious_request(self, request):
        """Check if request looks suspicious."""
        # Check for common attack patterns
        suspicious_patterns = [
            '../',
            '<script>',
            '1=1',
            'OR 1=1',
            'UNION SELECT',
            'DROP TABLE',
            'INSERT INTO',
            'EXEC(',
            'xp_cmdshell',
        ]
        
        # Check path, query string, and POST data
        for pattern in suspicious_patterns:
            if (pattern in request.path.lower() or
                pattern in request.GET.urlencode().lower() or
                (request.method == 'POST' and 
                 any(pattern in str(value).lower() for value in request.POST.values()))):
                return True
        
        return False
    
    def _log_suspicious_request(self, request):
        """Log suspicious request details."""
        user_info = f"User: {request.user.email if request.user.is_authenticated else 'Anonymous'}"
        ip_address = request.META.get('REMOTE_ADDR', 'unknown')
        user_agent = request.META.get('HTTP_USER_AGENT', 'unknown')
        
        logger.warning(
            f"Suspicious request detected: {user_info} from {ip_address} "
            f"using {user_agent}. Path: {request.path}"
        )