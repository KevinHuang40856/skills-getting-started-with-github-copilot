"""
Tests for the GET /activities endpoint.

These tests verify that the activities endpoint returns all activities
with the correct structure and data.
"""

import pytest


class TestGetActivities:
    """Tests for retrieving all activities."""

    def test_get_activities_returns_200(self, client):
        """Test that GET /activities returns a 200 status code."""
        response = client.get("/activities")
        assert response.status_code == 200

    def test_get_activities_returns_dict(self, client):
        """Test that GET /activities returns a dictionary."""
        response = client.get("/activities")
        assert isinstance(response.json(), dict)

    def test_get_activities_contains_all_hardcoded_activities(self, client):
        """Test that all 10 hardcoded activities are returned."""
        expected_activities = [
            "Chess Club",
            "Badminton Club",
            "Basketball Team",
            "Tennis Club",
            "Programming Class",
            "Debate Club",
            "Science Olympiad",
            "Gym Class",
            "Drama Club",
            "Art Studio"
        ]
        response = client.get("/activities")
        activities = response.json()
        
        for activity_name in expected_activities:
            assert activity_name in activities

    def test_get_activities_returns_exactly_ten_activities(self, client):
        """Test that exactly 10 activities are returned."""
        response = client.get("/activities")
        activities = response.json()
        assert len(activities) == 10

    def test_activity_has_required_fields(self, client, existing_activity):
        """Test that each activity has all required fields."""
        required_fields = ["description", "schedule", "max_participants", "participants"]
        response = client.get("/activities")
        activities = response.json()
        
        activity = activities[existing_activity]
        for field in required_fields:
            assert field in activity, f"Missing field: {field}"

    def test_activity_description_is_string(self, client, existing_activity):
        """Test that activity description is a string."""
        response = client.get("/activities")
        activities = response.json()
        activity = activities[existing_activity]
        assert isinstance(activity["description"], str)

    def test_activity_schedule_is_string(self, client, existing_activity):
        """Test that activity schedule is a string."""
        response = client.get("/activities")
        activities = response.json()
        activity = activities[existing_activity]
        assert isinstance(activity["schedule"], str)

    def test_activity_max_participants_is_integer(self, client, existing_activity):
        """Test that max_participants is an integer."""
        response = client.get("/activities")
        activities = response.json()
        activity = activities[existing_activity]
        assert isinstance(activity["max_participants"], int)

    def test_activity_participants_is_list(self, client, existing_activity):
        """Test that participants is a list."""
        response = client.get("/activities")
        activities = response.json()
        activity = activities[existing_activity]
        assert isinstance(activity["participants"], list)

    def test_activity_participants_are_strings(self, client, existing_activity):
        """Test that each participant email is a string."""
        response = client.get("/activities")
        activities = response.json()
        activity = activities[existing_activity]
        
        for email in activity["participants"]:
            assert isinstance(email, str)

    def test_get_activities_response_is_json(self, client):
        """Test that response can be parsed as JSON."""
        response = client.get("/activities")
        assert response.headers["content-type"] == "application/json"
