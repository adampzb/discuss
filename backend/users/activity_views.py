from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.utils import timezone
from datetime import timedelta
from .models import User
from .activity_models import UserActivity, UserActivityAggregation, UserSession
from .activity_serializers import (
    UserActivitySerializer,
    UserActivityAggregationSerializer,
    UserSessionSerializer,
    ActivityStatsSerializer
)


class StandardResultsSetPagination(PageNumberPagination):
    """Standard pagination for activity results."""
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100


class UserActivityListView(generics.ListAPIView):
    """
    View for listing user activities.
    """
    serializer_class = UserActivitySerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['activity_type', 'content_type']
    search_fields = ['activity_type', 'metadata']
    ordering_fields = ['created_at']
    ordering = ['-created_at']
    
    def get_queryset(self):
        # Users can only see their own activities
        return UserActivity.objects.filter(user=self.request.user)


class UserActivityDetailView(generics.RetrieveAPIView):
    """
    View for retrieving a specific user activity.
    """
    serializer_class = UserActivitySerializer
    
    def get_queryset(self):
        # Users can only see their own activities
        return UserActivity.objects.filter(user=self.request.user)


class UserActivityStatsView(generics.GenericAPIView):
    """
    View for getting user activity statistics.
    """
    
    def get(self, request, *args, **kwargs):
        user = request.user
        
        # Get activity statistics
        try:
            stats = user.activity_stats
        except UserActivityAggregation.DoesNotExist:
            stats = UserActivityAggregation.objects.create(user=user)
        
        # Get recent activities
        recent_activities = UserActivity.objects.filter(
            user=user
        ).order_by('-created_at')[:10]
        
        # Get activities by type
        activities_by_type = UserActivity.objects.filter(
            user=user
        ).values('activity_type').annotate(
            count=models.Count('activity_type')
        ).order_by('-count')
        
        activities_by_type_dict = {item['activity_type']: item['count'] for item in activities_by_type}
        
        # Get active sessions
        active_sessions = UserSession.objects.filter(
            user=user,
            is_active=True
        ).count()
        
        # Prepare response
        response_data = {
            'total_activities': stats.total_activities,
            'activities_by_type': activities_by_type_dict,
            'recent_activities': UserActivitySerializer(recent_activities, many=True).data,
            'active_sessions': active_sessions,
            'last_active': stats.last_active
        }
        
        return Response(response_data, status=status.HTTP_200_OK)


class UserActivityAggregationView(generics.RetrieveUpdateAPIView):
    """
    View for retrieving and updating user activity aggregation.
    """
    serializer_class = UserActivityAggregationSerializer
    
    def get_object(self):
        try:
            return self.request.user.activity_stats
        except UserActivityAggregation.DoesNotExist:
            return UserActivityAggregation.objects.create(user=self.request.user)


class UserSessionListView(generics.ListAPIView):
    """
    View for listing user sessions.
    """
    serializer_class = UserSessionSerializer
    
    def get_queryset(self):
        # Users can only see their own sessions
        return UserSession.objects.filter(user=self.request.user).order_by('-last_activity')


class UserSessionDetailView(generics.RetrieveDestroyAPIView):
    """
    View for retrieving and ending a user session.
    """
    serializer_class = UserSessionSerializer
    
    def get_queryset(self):
        # Users can only see their own sessions
        return UserSession.objects.filter(user=self.request.user)
    
    def delete(self, request, *args, **kwargs):
        """End a specific session."""
        instance = self.get_object()
        instance.end_session()
        return Response(
            {"detail": "Session ended successfully."},
            status=status.HTTP_200_OK
        )


class EndAllSessionsView(generics.GenericAPIView):
    """
    View for ending all user sessions except the current one.
    """
    
    def post(self, request, *args, **kwargs):
        current_session_key = request.session.session_key
        
        # End all sessions except current one
        sessions = UserSession.objects.filter(
            user=request.user,
            is_active=True
        ).exclude(session_key=current_session_key)
        
        session_count = sessions.count()
        sessions.update(is_active=False)
        
        return Response(
            {"detail": f"Ended {session_count} active sessions."},
            status=status.HTTP_200_OK
        )


class ActivityAnalyticsView(generics.GenericAPIView):
    """
    View for getting activity analytics and insights.
    """
    
    def get(self, request, *args, **kwargs):
        user = request.user
        
        # Time periods
        today = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
        this_week = today - timedelta(days=today.weekday())
        this_month = today.replace(day=1)
        
        # Calculate activity metrics
        metrics = {
            'today': {
                'start': today,
                'count': UserActivity.objects.filter(
                    user=user,
                    created_at__gte=today
                ).count()
            },
            'this_week': {
                'start': this_week,
                'count': UserActivity.objects.filter(
                    user=user,
                    created_at__gte=this_week
                ).count()
            },
            'this_month': {
                'start': this_month,
                'count': UserActivity.objects.filter(
                    user=user,
                    created_at__gte=this_month
                ).count()
            },
            'last_30_days': {
                'start': today - timedelta(days=30),
                'count': UserActivity.objects.filter(
                    user=user,
                    created_at__gte=today - timedelta(days=30)
                ).count()
            }
        }
        
        # Calculate engagement score (simple version)
        engagement_score = min(100, metrics['last_30_days']['count'] * 2)
        
        return Response({
            'metrics': metrics,
            'engagement_score': engagement_score,
            'activity_trend': 'stable'  # Could calculate actual trend
        }, status=status.HTTP_200_OK)