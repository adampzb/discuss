from rest_framework import serializers

from .activity_models import UserActivity, UserActivityAggregation, UserSession


class UserActivitySerializer(serializers.ModelSerializer):
    """
    Serializer for UserActivity model.
    """

    user_email = serializers.EmailField(source="user.email", read_only=True)
    activity_type_display = serializers.CharField(
        source="get_activity_type_display", read_only=True
    )

    class Meta:
        model = UserActivity
        fields = [
            "id",
            "user_email",
            "activity_type",
            "activity_type_display",
            "content_type",
            "object_id",
            "metadata",
            "ip_address",
            "user_agent",
            "created_at",
        ]
        read_only_fields = ["id", "user_email", "activity_type_display", "created_at"]


class UserActivityAggregationSerializer(serializers.ModelSerializer):
    """
    Serializer for UserActivityAggregation model.
    """

    class Meta:
        model = UserActivityAggregation
        fields = [
            "total_activities",
            "logins",
            "posts_created",
            "comments_created",
            "likes_received",
            "followers_gained",
            "current_streak",
            "longest_streak",
            "last_active",
            "show_activity",
        ]
        read_only_fields = ["total_activities", "last_active"]


class UserSessionSerializer(serializers.ModelSerializer):
    """
    Serializer for UserSession model.
    """

    user_email = serializers.EmailField(source="user.email", read_only=True)

    class Meta:
        model = UserSession
        fields = [
            "id",
            "user_email",
            "session_key",
            "ip_address",
            "country",
            "city",
            "is_active",
            "created_at",
            "last_activity",
        ]
        read_only_fields = [
            "id",
            "user_email",
            "session_key",
            "created_at",
            "last_activity",
        ]


class ActivityStatsSerializer(serializers.Serializer):
    """
    Serializer for activity statistics.
    """

    total_activities = serializers.IntegerField()
    activities_by_type = serializers.DictField()
    recent_activities = UserActivitySerializer(many=True)
    active_sessions = serializers.IntegerField()
    last_active = serializers.DateTimeField()
