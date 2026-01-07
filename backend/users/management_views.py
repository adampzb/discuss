from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, permissions, status
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from .profile_models import UserProfile
from .profile_serializers import UserProfileSerializer
from .serializers import UserSerializer

User = get_user_model()


class StandardResultsSetPagination(PageNumberPagination):
    """
    Standard pagination for API results.
    """

    page_size = 20
    page_size_query_param = "page_size"
    max_page_size = 100


class UserListView(generics.ListAPIView):
    """
    View for listing users (admin only).
    """

    serializer_class = UserSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["is_active", "is_staff", "is_superuser"]
    search_fields = ["email", "first_name", "last_name"]
    ordering_fields = [
        "id",
        "email",
        "first_name",
        "last_name",
        "date_joined",
        "last_login",
    ]
    ordering = ["-date_joined"]

    def get_queryset(self):
        # Only allow staff users to access this endpoint
        if not self.request.user.is_staff:
            return User.objects.none()

        return User.objects.all()


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    View for retrieving, updating, and deleting user details (admin only).
    """

    serializer_class = UserSerializer

    def get_queryset(self):
        # Only allow staff users to access this endpoint
        if not self.request.user.is_staff:
            return User.objects.none()

        return User.objects.all()


class UserActivationView(generics.GenericAPIView):
    """
    View for activating/deactivating users (admin only).
    """

    permission_classes = [permissions.IsAdminUser]

    def post(self, request, user_id, *args, **kwargs):
        try:
            user = User.objects.get(id=user_id)
            action = request.data.get("action", "toggle")

            if action == "activate":
                user.is_active = True
                message = f"User {user.email} has been activated."
            elif action == "deactivate":
                user.is_active = False
                message = f"User {user.email} has been deactivated."
            else:  # toggle
                user.is_active = not user.is_active
                status = "activated" if user.is_active else "deactivated"
                message = f"User {user.email} has been {status}."

            user.save()
            return Response({"detail": message}, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response(
                {"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND
            )


class UserStatsView(generics.GenericAPIView):
    """
    View for getting user statistics (admin only).
    """

    permission_classes = [permissions.IsAdminUser]

    def get(self, request, *args, **kwargs):
        stats = {
            "total_users": User.objects.count(),
            "active_users": User.objects.filter(is_active=True).count(),
            "inactive_users": User.objects.filter(is_active=False).count(),
            "staff_users": User.objects.filter(is_staff=True).count(),
            "superusers": User.objects.filter(is_superuser=True).count(),
            "recent_users": User.objects.filter(is_active=True)
            .order_by("-date_joined")[:5]
            .values("id", "email", "first_name", "last_name", "date_joined"),
        }

        return Response(stats, status=status.HTTP_200_OK)


class UserProfileManagementView(generics.RetrieveUpdateAPIView):
    """
    View for managing user profiles (admin only).
    """

    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAdminUser]

    def get_queryset(self):
        return UserProfile.objects.all()


class UserExportView(generics.GenericAPIView):
    """
    View for exporting user data (admin only).
    """

    permission_classes = [permissions.IsAdminUser]

    def get(self, request, *args, **kwargs):
        # Get filter parameters
        is_active = request.query_params.get("is_active")
        is_staff = request.query_params.get("is_staff")

        # Build queryset
        queryset = User.objects.all()

        if is_active is not None:
            queryset = queryset.filter(is_active=is_active.lower() == "true")

        if is_staff is not None:
            queryset = queryset.filter(is_staff=is_staff.lower() == "true")

        # Prepare export data
        export_data = []
        for user in queryset:
            export_data.append(
                {
                    "id": user.id,
                    "email": user.email,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "is_active": user.is_active,
                    "is_staff": user.is_staff,
                    "is_superuser": user.is_superuser,
                    "date_joined": user.date_joined,
                    "last_login": user.last_login,
                }
            )

        return Response(
            {"count": len(export_data), "data": export_data}, status=status.HTTP_200_OK
        )
