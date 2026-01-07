from django.urls import path

from .management_views import (
    UserActivationView,
    UserDetailView,
    UserExportView,
    UserListView,
    UserProfileManagementView,
    UserStatsView,
)

urlpatterns = [
    # User management endpoints (admin only)
    path("users/", UserListView.as_view(), name="user-list"),
    path("users/<int:pk>/", UserDetailView.as_view(), name="user-detail"),
    path(
        "users/<int:user_id>/activate/",
        UserActivationView.as_view(),
        name="user-activate",
    ),
    path("users/stats/", UserStatsView.as_view(), name="user-stats"),
    # Profile management endpoints (admin only)
    path(
        "profiles/<int:pk>/",
        UserProfileManagementView.as_view(),
        name="profile-management",
    ),
    # Data export endpoints (admin only)
    path("users/export/", UserExportView.as_view(), name="user-export"),
]
