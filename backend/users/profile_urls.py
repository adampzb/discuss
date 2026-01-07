from django.urls import path

from .profile_views import BlockView, FollowView, UserProfileDetailView, UserSearchView

urlpatterns = [
    # Profile endpoints
    path("profile/", UserProfileDetailView.as_view(), name="profile-detail"),
    path(
        "profile/<int:user_id>/",
        UserProfileDetailView.as_view(),
        name="user-profile-detail",
    ),
    # Social endpoints
    path("follow/", FollowView.as_view(), name="follow-user"),
    path("block/", BlockView.as_view(), name="block-user"),
    # Search endpoints
    path("search/", UserSearchView.as_view(), name="user-search"),
]
