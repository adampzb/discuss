from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from .profile_models import UserProfile

User = get_user_model()


class AuthenticationTests(TestCase):
    """
    Test authentication functionality.
    """

    def setUp(self):
        self.client = APIClient()
        self.user_data = {
            "email": "test@example.com",
            "password": "testpassword123",
            "password_confirmation": "testpassword123",
            "first_name": "Test",
            "last_name": "User",
        }

        # Create a test user
        self.user = User.objects.create_user(
            email="existing@example.com",
            password="existingpassword123",
            first_name="Existing",
            last_name="User",
        )

    def test_user_registration(self):
        """Test user registration endpoint."""
        response = self.client.post(
            reverse("user-register"), self.user_data, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("user", response.data)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

        # Verify user was created
        self.assertTrue(User.objects.filter(email="test@example.com").exists())

    def test_user_login(self):
        """Test user login endpoint."""
        login_data = {
            "email": "existing@example.com",
            "password": "existingpassword123",
        }

        response = self.client.post(
            reverse("token_obtain_pair"), login_data, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)
        self.assertIn("user", response.data)

    def test_token_refresh(self):
        """Test token refresh endpoint."""
        # First, get a token
        login_data = {
            "email": "existing@example.com",
            "password": "existingpassword123",
        }

        login_response = self.client.post(
            reverse("token_obtain_pair"), login_data, format="json"
        )
        refresh_token = login_response.data["refresh"]

        # Now refresh the token
        refresh_data = {"refresh": refresh_token}
        response = self.client.post(
            reverse("token_refresh"), refresh_data, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)

    def test_password_reset_request(self):
        """Test password reset request endpoint."""
        reset_data = {"email": "existing@example.com"}

        response = self.client.post(
            reverse("password-reset"), reset_data, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("detail", response.data)

    def test_user_profile_retrieval(self):
        """Test user profile retrieval endpoint."""
        # First, authenticate
        login_data = {
            "email": "existing@example.com",
            "password": "existingpassword123",
        }

        login_response = self.client.post(
            reverse("token_obtain_pair"), login_data, format="json"
        )
        access_token = login_response.data["access"]

        # Now retrieve profile
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")
        response = self.client.get(reverse("user-profile"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], "existing@example.com")


class UserProfileTests(TestCase):
    """
    Test user profile functionality.
    """

    def setUp(self):
        self.client = APIClient()

        # Create test users
        self.user1 = User.objects.create_user(
            email="user1@example.com",
            password="password123",
            first_name="User",
            last_name="One",
        )

        self.user2 = User.objects.create_user(
            email="user2@example.com",
            password="password123",
            first_name="User",
            last_name="Two",
        )

        # Get profiles (they should be created automatically by signals)
        self.profile1 = self.user1.profile
        self.profile2 = self.user2.profile

    def test_profile_creation_on_user_creation(self):
        """Test that profile is automatically created when user is created."""
        # Create a new user
        new_user = User.objects.create_user(
            email="newuser@example.com", password="password123"
        )

        # Check if profile was created
        self.assertTrue(UserProfile.objects.filter(user=new_user).exists())

    def test_profile_retrieval(self):
        """Test profile retrieval endpoint."""
        # Authenticate user1
        login_data = {"email": "user1@example.com", "password": "password123"}

        login_response = self.client.post(
            reverse("token_obtain_pair"), login_data, format="json"
        )
        access_token = login_response.data["access"]

        # Retrieve own profile
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")
        response = self.client.get(reverse("profile-detail"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["user"]["email"], "user1@example.com")

    def test_follow_functionality(self):
        """Test follow/unfollow functionality."""
        # Authenticate user1
        login_data = {"email": "user1@example.com", "password": "password123"}

        login_response = self.client.post(
            reverse("token_obtain_pair"), login_data, format="json"
        )
        access_token = login_response.data["access"]

        # Follow user2
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")
        follow_data = {"user_id": self.user2.id, "action": "follow"}

        response = self.client.post(reverse("follow-user"), follow_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(self.profile1.is_following(self.user2))

        # Unfollow user2
        follow_data["action"] = "unfollow"
        response = self.client.post(reverse("follow-user"), follow_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(self.profile1.is_following(self.user2))

    def test_user_search(self):
        """Test user search functionality."""
        # Authenticate user1
        login_data = {"email": "user1@example.com", "password": "password123"}

        login_response = self.client.post(
            reverse("token_obtain_pair"), login_data, format="json"
        )
        access_token = login_response.data["access"]

        # Search for users
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")
        response = self.client.get(reverse("user-search"), {"q": "user2@example.com"})

        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["email"], "user2@example.com")


class UserManagementTests(TestCase):
    """
    Test user management functionality (admin only).
    """

    def setUp(self):
        self.client = APIClient()

        # Create admin user
        self.admin_user = User.objects.create_superuser(
            email="admin@example.com",
            password="adminpassword123",
            first_name="Admin",
            last_name="User",
        )

        # Create regular user
        self.regular_user = User.objects.create_user(
            email="regular@example.com",
            password="regularpassword123",
            first_name="Regular",
            last_name="User",
        )

    def test_user_list_admin_only(self):
        """Test that only admin users can access user list."""
        # Try with regular user
        login_data = {"email": "regular@example.com", "password": "regularpassword123"}

        login_response = self.client.post(
            reverse("token_obtain_pair"), login_data, format="json"
        )
        access_token = login_response.data["access"]

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")
        response = self.client.get(reverse("user-list"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            len(response.data["results"]), 0
        )  # Regular users get empty results

        # Try with admin user
        login_data = {"email": "admin@example.com", "password": "adminpassword123"}

        login_response = self.client.post(
            reverse("token_obtain_pair"), login_data, format="json"
        )
        access_token = login_response.data["access"]

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")
        response = self.client.get(reverse("user-list"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 2)  # Admin gets all users

    def test_user_activation_deactivation(self):
        """Test user activation/deactivation functionality."""
        # Authenticate as admin
        login_data = {"email": "admin@example.com", "password": "adminpassword123"}

        login_response = self.client.post(
            reverse("token_obtain_pair"), login_data, format="json"
        )
        access_token = login_response.data["access"]

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")

        # Deactivate user
        response = self.client.post(
            reverse("user-activate", kwargs={"user_id": self.regular_user.id}),
            {"action": "deactivate"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check if user was deactivated
        self.regular_user.refresh_from_db()
        self.assertFalse(self.regular_user.is_active)

        # Activate user
        response = self.client.post(
            reverse("user-activate", kwargs={"user_id": self.regular_user.id}),
            {"action": "activate"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check if user was activated
        self.regular_user.refresh_from_db()
        self.assertTrue(self.regular_user.is_active)

    def test_user_stats(self):
        """Test user statistics endpoint."""
        # Authenticate as admin
        login_data = {"email": "admin@example.com", "password": "adminpassword123"}

        login_response = self.client.post(
            reverse("token_obtain_pair"), login_data, format="json"
        )
        access_token = login_response.data["access"]

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")
        response = self.client.get(reverse("user-stats"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("total_users", response.data)
        self.assertIn("active_users", response.data)
        self.assertIn("staff_users", response.data)
        self.assertEqual(response.data["total_users"], 2)
