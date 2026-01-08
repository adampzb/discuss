from rest_framework import serializers

from .models import User
from .profile_models import UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for UserProfile model.
    """

    user = serializers.SerializerMethodField()
    followers_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = [
            "id",
            "user",
            "privacy_setting",
            "email_notifications",
            "push_notifications",
            "website",
            "github_username",
            "twitter_username",
            "linkedin_username",
            "location",
            "occupation",
            "company",
            "theme_preference",
            "language_preference",
            "profile_background",
            "followers_count",
            "following_count",
            "last_active",
            "date_created",
        ]
        read_only_fields = [
            "id",
            "last_active",
            "date_created",
            "followers_count",
            "following_count",
        ]

    def get_user(self, obj):
        """Get user data for the profile."""
        return {
            "id": obj.user.id,
            "email": obj.user.email,
            "first_name": obj.user.first_name,
            "last_name": obj.user.last_name,
            "bio": obj.user.bio,
            "profile_picture": obj.user.profile_picture.url if obj.user.profile_picture else None,
            "date_of_birth": obj.user.date_of_birth,
        }

    def get_followers_count(self, obj):
        return obj.get_followers_count()

    def get_following_count(self, obj):
        return obj.get_following_count()

    def update(self, instance, validated_data):
        """
        Update both User and UserProfile instances.
        """
        # Extract user data
        user_data = validated_data.pop("user", {})

        # Update user fields
        user = instance.user
        for field, value in user_data.items():
            setattr(user, field, value)
        user.save()

        # Update profile fields
        for field, value in validated_data.items():
            setattr(instance, field, value)
        instance.save()

        return instance


class FollowSerializer(serializers.Serializer):
    """
    Serializer for follow/unfollow actions.
    """

    user_id = serializers.IntegerField(required=True)
    action = serializers.ChoiceField(choices=["follow", "unfollow"], required=True)


class BlockSerializer(serializers.Serializer):
    """
    Serializer for block/unblock actions.
    """

    user_id = serializers.IntegerField(required=True)
    action = serializers.ChoiceField(choices=["block", "unblock"], required=True)


class UserSearchSerializer(serializers.ModelSerializer):
    """
    Serializer for user search results.
    """

    profile_picture = serializers.ImageField(required=False)
    is_following = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "profile_picture",
            "is_following",
        ]

    def get_is_following(self, obj):
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            return obj.followers.filter(id=request.user.id).exists()
        return False
