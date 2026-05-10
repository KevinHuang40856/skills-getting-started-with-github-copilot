"""
Tests for the DELETE /activities/{activity_name}/signup endpoint.

These tests verify unregister/unsignup functionality including happy path
and error handling (not registered, non-existent activities, etc).
"""

import pytest


class TestUnsignupFromActivity:
    """Tests for unregistering from activities."""

    def test_unsignup_returns_200(self, client, existing_activity):
        """Test that a valid unsignup returns 200 status code."""
        email = "unsignup.test@mergington.edu"
        
        # First sign up
        client.post(
            f"/activities/{existing_activity}/signup",
            params={"email": email}
        )
        
        # Then unsignup
        response = client.delete(
            f"/activities/{existing_activity}/signup",
            params={"email": email}
        )
        assert response.status_code == 200

    def test_unsignup_returns_success_message(self, client, existing_activity):
        """Test that unsignup returns a success message."""
        email = "unsignup.test@mergington.edu"
        
        # Sign up first
        client.post(
            f"/activities/{existing_activity}/signup",
            params={"email": email}
        )
        
        # Unsignup
        response = client.delete(
            f"/activities/{existing_activity}/signup",
            params={"email": email}
        )
        data = response.json()
        assert "message" in data
        assert email in data["message"]
        assert existing_activity in data["message"]

    def test_unsignup_removes_student_from_participants(self, client, existing_activity):
        """Test that unsignup removes the student from participants list."""
        email = "unsignup.test@mergington.edu"
        
        # Sign up
        client.post(
            f"/activities/{existing_activity}/signup",
            params={"email": email}
        )
        
        # Verify student is in participants
        response = client.get("/activities")
        assert email in response.json()[existing_activity]["participants"]
        
        # Unsignup
        client.delete(
            f"/activities/{existing_activity}/signup",
            params={"email": email}
        )
        
        # Verify student was removed
        response = client.get("/activities")
        assert email not in response.json()[existing_activity]["participants"]

    def test_unsignup_from_nonexistent_activity_returns_404(self, client, non_existent_activity):
        """Test that unsignup from non-existent activity returns 404."""
        email = "test@mergington.edu"
        response = client.delete(
            f"/activities/{non_existent_activity}/signup",
            params={"email": email}
        )
        assert response.status_code == 404

    def test_unsignup_from_nonexistent_activity_returns_error(self, client, non_existent_activity):
        """Test that unsignup from non-existent activity returns error message."""
        email = "test@mergington.edu"
        response = client.delete(
            f"/activities/{non_existent_activity}/signup",
            params={"email": email}
        )
        data = response.json()
        assert "detail" in data
        assert "not found" in data["detail"].lower()

    def test_unsignup_when_not_signed_up_returns_400(self, client, existing_activity):
        """Test that unregistering without being signed up returns 400."""
        email = "never.signed.up@mergington.edu"
        response = client.delete(
            f"/activities/{existing_activity}/signup",
            params={"email": email}
        )
        assert response.status_code == 400

    def test_unsignup_when_not_signed_up_returns_error_message(self, client, existing_activity):
        """Test that unsignup without being signed up returns appropriate error."""
        email = "never.signed.up@mergington.edu"
        response = client.delete(
            f"/activities/{existing_activity}/signup",
            params={"email": email}
        )
        data = response.json()
        assert "detail" in data
        assert "not signed up" in data["detail"].lower()

    def test_unsignup_twice_returns_400_second_time(self, client, existing_activity):
        """Test that unregistering twice returns 400 on the second attempt."""
        email = "double.unsignup@mergington.edu"
        
        # Sign up
        client.post(
            f"/activities/{existing_activity}/signup",
            params={"email": email}
        )
        
        # First unsignup succeeds
        response1 = client.delete(
            f"/activities/{existing_activity}/signup",
            params={"email": email}
        )
        assert response1.status_code == 200
        
        # Second unsignup fails
        response2 = client.delete(
            f"/activities/{existing_activity}/signup",
            params={"email": email}
        )
        assert response2.status_code == 400

    def test_unsignup_email_parameter_required(self, client, existing_activity):
        """Test that email parameter is required for unsignup."""
        response = client.delete(f"/activities/{existing_activity}/signup")
        # Missing required query parameter should return 422
        assert response.status_code == 422

    def test_unsignup_activity_name_with_spaces(self, client):
        """Test that unsignup works with activity names containing spaces."""
        activity_with_spaces = "Basketball Team"
        email = "basketball.fan@mergington.edu"
        
        # Sign up
        client.post(
            f"/activities/{activity_with_spaces}/signup",
            params={"email": email}
        )
        
        # Unsignup
        response = client.delete(
            f"/activities/{activity_with_spaces}/signup",
            params={"email": email}
        )
        assert response.status_code == 200

    def test_signup_nonsignup_signup_sequence(self, client, existing_activity):
        """Test signup -> unsignup -> signup sequence works correctly."""
        email = "sequence.test@mergington.edu"
        
        # Sign up
        client.post(
            f"/activities/{existing_activity}/signup",
            params={"email": email}
        )
        response1 = client.get("/activities")
        assert email in response1.json()[existing_activity]["participants"]
        
        # Unsignup
        client.delete(
            f"/activities/{existing_activity}/signup",
            params={"email": email}
        )
        response2 = client.get("/activities")
        assert email not in response2.json()[existing_activity]["participants"]
        
        # Sign up again
        client.post(
            f"/activities/{existing_activity}/signup",
            params={"email": email}
        )
        response3 = client.get("/activities")
        assert email in response3.json()[existing_activity]["participants"]
