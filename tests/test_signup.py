"""
Tests for the POST /activities/{activity_name}/signup endpoint.

These tests verify signup functionality including happy path scenarios
and error handling (duplicate signups, non-existent activities, etc).
"""

import pytest


class TestSignupForActivity:
    """Tests for signing up for activities."""

    def test_signup_returns_200(self, client, existing_activity, sample_email):
        """Test that a valid signup returns 200 status code."""
        response = client.post(
            f"/activities/{existing_activity}/signup",
            params={"email": sample_email}
        )
        assert response.status_code == 200

    def test_signup_returns_success_message(self, client, existing_activity, sample_email):
        """Test that signup returns a success message."""
        response = client.post(
            f"/activities/{existing_activity}/signup",
            params={"email": sample_email}
        )
        data = response.json()
        assert "message" in data
        assert sample_email in data["message"]
        assert existing_activity in data["message"]

    def test_signup_adds_student_to_participants(self, client, existing_activity, sample_email):
        """Test that signup adds the student to the participants list."""
        # Get initial participants
        initial_response = client.get("/activities")
        initial_participants = initial_response.json()[existing_activity]["participants"]
        initial_count = len(initial_participants)

        # Sign up
        client.post(
            f"/activities/{existing_activity}/signup",
            params={"email": sample_email}
        )

        # Verify student was added
        updated_response = client.get("/activities")
        updated_participants = updated_response.json()[existing_activity]["participants"]
        
        assert sample_email in updated_participants
        assert len(updated_participants) == initial_count + 1

    def test_signup_to_nonexistent_activity_returns_404(self, client, non_existent_activity, sample_email):
        """Test that signup to non-existent activity returns 404."""
        response = client.post(
            f"/activities/{non_existent_activity}/signup",
            params={"email": sample_email}
        )
        assert response.status_code == 404

    def test_signup_to_nonexistent_activity_returns_error_message(self, client, non_existent_activity, sample_email):
        """Test that signup to non-existent activity returns appropriate error."""
        response = client.post(
            f"/activities/{non_existent_activity}/signup",
            params={"email": sample_email}
        )
        data = response.json()
        assert "detail" in data
        assert "not found" in data["detail"].lower()

    def test_duplicate_signup_returns_400(self, client, existing_activity):
        """Test that signing up twice with the same email returns 400."""
        # First signup
        email = "duplicate.test@mergington.edu"
        client.post(
            f"/activities/{existing_activity}/signup",
            params={"email": email}
        )

        # Second signup (duplicate)
        response = client.post(
            f"/activities/{existing_activity}/signup",
            params={"email": email}
        )
        assert response.status_code == 400

    def test_duplicate_signup_returns_error_message(self, client, existing_activity):
        """Test that duplicate signup returns appropriate error message."""
        email = "duplicate.test@mergington.edu"
        client.post(
            f"/activities/{existing_activity}/signup",
            params={"email": email}
        )

        response = client.post(
            f"/activities/{existing_activity}/signup",
            params={"email": email}
        )
        data = response.json()
        assert "detail" in data
        assert "already signed up" in data["detail"].lower()

    def test_signup_with_different_emails_succeeds(self, client, existing_activity):
        """Test that multiple different students can sign up for same activity."""
        email1 = "student1@mergington.edu"
        email2 = "student2@mergington.edu"

        response1 = client.post(
            f"/activities/{existing_activity}/signup",
            params={"email": email1}
        )
        response2 = client.post(
            f"/activities/{existing_activity}/signup",
            params={"email": email2}
        )

        assert response1.status_code == 200
        assert response2.status_code == 200

        # Verify both are in participants
        activities_response = client.get("/activities")
        participants = activities_response.json()[existing_activity]["participants"]
        assert email1 in participants
        assert email2 in participants

    def test_signup_with_special_characters_in_email(self, client, existing_activity):
        """Test that signup works with special characters in email."""
        email = "student+tag@mergington.edu"
        response = client.post(
            f"/activities/{existing_activity}/signup",
            params={"email": email}
        )
        assert response.status_code == 200

    def test_signup_email_parameter_required(self, client, existing_activity):
        """Test that email parameter is required."""
        response = client.post(f"/activities/{existing_activity}/signup")
        # Missing required query parameter should return 422
        assert response.status_code == 422

    def test_signup_activity_name_with_spaces(self, client):
        """Test that signup works with activity names containing spaces."""
        activity_with_spaces = "Basketball Team"
        email = "basketball.fan@mergington.edu"
        response = client.post(
            f"/activities/{activity_with_spaces}/signup",
            params={"email": email}
        )
        assert response.status_code == 200
