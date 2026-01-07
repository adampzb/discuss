from django.urls import path

from .activity_views import (
    ActivityAnalyticsView,
    EndAllSessionsView,
    UserActivityAggregationView,
    UserActivityDetailView,
    UserActivityListView,
    UserActivityStatsView,
    UserSessionDetailView,
    UserSessionListView,
)

urlpatterns = [
    # Activity endpoints
    path("activities/", UserActivityListView.as_view(), name="activity-list"),
    path(
        "activities/<int:pk>/", UserActivityDetailView.as_view(), name="activity-detail"
    ),
    path("activities/stats/", UserActivityStatsView.as_view(), name="activity-stats"),
    path(
        "activities/aggregation/",
        UserActivityAggregationView.as_view(),
        name="activity-aggregation",
    ),
    # Session endpoints
    path("sessions/", UserSessionListView.as_view(), name="session-list"),
    path("sessions/<int:pk>/", UserSessionDetailView.as_view(), name="session-detail"),
    path("sessions/end-all/", EndAllSessionsView.as_view(), name="end-all-sessions"),
    # Analytics endpoints
    path("analytics/", ActivityAnalyticsView.as_view(), name="activity-analytics"),
]
