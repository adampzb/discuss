from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """
    User serializer for registration and profile management.
    """

    password = serializers.CharField(
        write_only=True, required=True, style={"input_type": "password"}
    )
    password_confirmation = serializers.CharField(
        write_only=True, required=True, style={"input_type": "password"}
    )

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "password",
            "password_confirmation",
            "bio",
            "profile_picture",
            "date_of_birth",
            "is_active",
            "is_staff",
        ]
        read_only_fields = ["id", "is_active", "is_staff"]
        extra_kwargs = {
            "email": {"required": True},
            "first_name": {"required": False},
            "last_name": {"required": False},
        }

    def validate(self, data):
        """
        Validate that passwords match.
        """
        if data["password"] != data["password_confirmation"]:
            raise serializers.ValidationError(
                {"password_confirmation": "Passwords do not match."}
            )
        return data

    def create(self, validated_data):
        """
        Create and return a new user.
        """
        # Remove password_confirmation from validated data
        validated_data.pop("password_confirmation")

        # Create user
        user = User.objects.create_user(
            email=validated_data["email"],
            password=validated_data["password"],
            first_name=validated_data.get("first_name", ""),
            last_name=validated_data.get("last_name", ""),
        )

        # Set additional fields if provided
        if "bio" in validated_data:
            user.bio = validated_data["bio"]
        if "date_of_birth" in validated_data:
            user.date_of_birth = validated_data["date_of_birth"]

        user.save()
        return user

    def update(self, instance, validated_data):
        """
        Update and return an existing user.
        """
        # Remove password_confirmation from validated data
        validated_data.pop("password_confirmation", None)

        # Handle password update separately
        password = validated_data.pop("password", None)

        # Update other fields
        for field, value in validated_data.items():
            setattr(instance, field, value)

        # Update password if provided
        if password:
            instance.set_password(password)

        instance.save()
        return instance


class PasswordResetSerializer(serializers.Serializer):
    """
    Serializer for password reset requests.
    """

    email = serializers.EmailField(required=True)


class SetNewPasswordSerializer(serializers.Serializer):
    """
    Serializer for setting new password.
    """

    password = serializers.CharField(
        write_only=True, required=True, style={"input_type": "password"}
    )
    password_confirmation = serializers.CharField(
        write_only=True, required=True, style={"input_type": "password"}
    )

    def validate(self, data):
        """
        Validate that passwords match and meet requirements.
        """
        if data["password"] != data["password_confirmation"]:
            raise serializers.ValidationError(
                {"password_confirmation": "Passwords do not match."}
            )

        # Validate password strength
        try:
            validate_password(data["password"])
        except ValidationError as e:
            raise serializers.ValidationError({"password": e.messages})

        return data
