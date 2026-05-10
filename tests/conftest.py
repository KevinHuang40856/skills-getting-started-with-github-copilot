"""
Test configuration and shared fixtures for FastAPI backend tests.

This module provides reusable fixtures for testing the Mergington High School API,
including a TestClient and activity data fixtures.
"""

import pytest
from copy import deepcopy
from fastapi.testclient import TestClient
from src import app as app_module


# Store original activities data
ORIGINAL_ACTIVITIES = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "Badminton Club": {
        "description": "Learn strategies and compete in badminton tournaments",
        "schedule": "Fridays, 1:30 PM - 3:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "Basketball Team": {
        "description": "Join our competitive basketball team and compete in tournaments",
        "schedule": "Mondays and Wednesdays, 4:00 PM - 5:30 PM",
        "max_participants": 15,
        "participants": ["alex@mergington.edu","daniel@mergington.edu"]
    },
    "Tennis Club": {
        "description": "Learn tennis skills and play matches",
        "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:30 PM",
        "max_participants": 16,
        "participants": ["sarah@mergington.edu", "james@mergington.edu"]
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    "Debate Club": {
        "description": "Develop argumentation and public speaking skills through debates",
        "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
        "max_participants": 25,
        "participants": ["liam@mergington.edu"]
    },
    "Science Olympiad": {
        "description": "Compete in science competitions and experiments",
        "schedule": "Saturdays, 10:00 AM - 12:00 PM",
        "max_participants": 20,
        "participants": ["maya@mergington.edu", "noah@mergington.edu"]
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    },
    "Drama Club": {
        "description": "Perform in school plays and develop acting skills",
        "schedule": "Thursdays, 3:30 PM - 5:00 PM",
        "max_participants": 30,
        "participants": ["lucas@mergington.edu"]
    },
    "Art Studio": {
        "description": "Explore painting, drawing, and sculpture techniques",
        "schedule": "Mondays, 4:00 PM - 5:30 PM",
        "max_participants": 18,
        "participants": ["ava@mergington.edu", "isabella@mergington.edu"]
    }
}


@pytest.fixture
def client():
    """
    Provides a FastAPI TestClient for making test requests to the app.
    Resets the app's in-memory activities data before each test to ensure test isolation.
    Uses deep copy to avoid sharing mutable list objects between tests.
    """
    # Reset activities to original state before each test with deep copy for isolation
    app_module.activities.clear()
    app_module.activities.update(deepcopy(ORIGINAL_ACTIVITIES))
    
    return TestClient(app_module.app)


@pytest.fixture
def sample_email():
    """A sample student email for use in tests."""
    return "test.student@mergington.edu"


@pytest.fixture
def existing_activity():
    """Returns the name of an activity that exists in the hardcoded data."""
    return "Chess Club"


@pytest.fixture
def non_existent_activity():
    """Returns a name of an activity that does not exist."""
    return "Nonexistent Activity"
