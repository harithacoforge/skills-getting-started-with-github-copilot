"""Tests for POST /activities/{activity_name}/signup endpoint using AAA pattern"""

import pytest


@pytest.mark.parametrize("activity_name,email,expected_status,expected_message", [
    # Happy path
    ("Basketball Team", "test@example.com", 200, "Signed up test@example.com for Basketball Team"),
    # Activity not found
    ("Nonexistent Activity", "test@example.com", 404, "Activity not found"),
    # Already signed up
    ("Chess Club", "michael@mergington.edu", 400, "Student already signed up for this activity"),
])
def test_signup_scenarios(client, activity_name, email, expected_status, expected_message):
    """Test various signup scenarios using AAA pattern"""
    # Arrange: Test client and test data provided via parametrize

    # Act: POST to signup endpoint
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert: Check status code and response message
    assert response.status_code == expected_status
    data = response.json()
    if expected_status == 200:
        assert data["message"] == expected_message
    else:
        assert data["detail"] == expected_message


def test_signup_adds_participant(client):
    """Test that successful signup adds participant to activity"""
    # Arrange
    activity_name = "Basketball Team"
    email = "newstudent@example.com"

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert
    assert response.status_code == 200
    # Verify participant was added
    activities_response = client.get("/activities")
    activities_data = activities_response.json()
    assert email in activities_data[activity_name]["participants"]