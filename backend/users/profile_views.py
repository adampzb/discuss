from django.contrib.auth import get_user_model
from django.db import models
from rest_framework import generics, permissions, status
from rest_framework.response import Response

from .profile_models import UserProfile
from .profile_serializers import (
    BlockSerializer,
    FollowSerializer,
    UserProfileSerializer,
    UserSearchSerializer,
)

User = get_user_model()


class UserProfileDetailView(generics.RetrieveUpdateAPIView):
    """
    View for retrieving and updating user profile details.
    """

    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        # Allow users to view their own profile or public profiles
        user_id = self.kwargs.get("user_id")

        if user_id:
            # Check if user is trying to access their own profile
            if self.request.user.id == user_id:
                return self.request.user.profile

            # Check if profile is public or user is following
            try:
                profile = UserProfile.objects.get(user_id=user_id)

                # Check privacy settings
                if profile.privacy_setting == "public":
                    return profile
                elif profile.privacy_setting == "friends" and profile.is_following(
                    self.request.user
                ):
                    return profile
                else:
                    return Response(
                        {"detail": "This profile is private."},
                        status=status.HTTP_403_FORBIDDEN,
                    )
            except UserProfile.DoesNotExist:
                return Response(
                    {"detail": "User profile not found."},
                    status=status.HTTP_404_NOT_FOUND,
                )

        # Default to current user's profile
        return self.request.user.profile

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["request"] = self.request
        return context


class FollowView(generics.GenericAPIView):
    """
    View for following/unfollowing users.
    """

    serializer_class = FollowSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user_id = serializer.validated_data["user_id"]
        action = serializer.validated_data["action"]

        try:
            target_user = User.objects.get(id=user_id)
            profile = request.user.profile

            if action == "follow":
                if profile.toggle_follow(target_user):
                    return Response(
                        {"detail": f"You are now following {target_user.email}."},
                        status=status.HTTP_200_OK,
                    )
                else:
                    return Response(
                        {"detail": f"You have unfollowed {target_user.email}."},
                        status=status.HTTP_200_OK,
                    )
            else:
                if not profile.toggle_follow(target_user):
                    return Response(
                        {"detail": f"You have unfollowed {target_user.email}."},
                        status=status.HTTP_200_OK,
                    )
                else:
                    return Response(
                        {"detail": f"You are now following {target_user.email}."},
                        status=status.HTTP_200_OK,
                    )

        except User.DoesNotExist:
            return Response(
                {"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND
            )


class BlockView(generics.GenericAPIView):
    """
    View for blocking/unblocking users.
    """

    serializer_class = BlockSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user_id = serializer.validated_data["user_id"]
        action = serializer.validated_data["action"]

        try:
            target_user = User.objects.get(id=user_id)
            profile = request.user.profile

            if action == "block":
                if profile.toggle_block(target_user):
                    return Response(
                        {"detail": f"You have blocked {target_user.email}."},
                        status=status.HTTP_200_OK,
                    )
                else:
                    return Response(
                        {"detail": f"You have unblocked {target_user.email}."},
                        status=status.HTTP_200_OK,
                    )
            else:
                if not profile.toggle_block(target_user):
                    return Response(
                        {"detail": f"You have unblocked {target_user.email}."},
                        status=status.HTTP_200_OK,
                    )
                else:
                    return Response(
                        {"detail": f"You have blocked {target_user.email}."},
                        status=status.HTTP_200_OK,
                    )

        except User.DoesNotExist:
            return Response(
                {"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND
            )


class UserSearchView(generics.ListAPIView):
    """
    View for searching users.
    """

    serializer_class = UserSearchSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        query = self.request.query_params.get("q", "")

        if query:
            return User.objects.filter(
                models.Q(email__icontains=query)
                | models.Q(first_name__icontains=query)
                | models.Q(last_name__icontains=query)
            ).exclude(id=self.request.user.id)

        return User.objects.none()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["request"] = self.request
        return context
