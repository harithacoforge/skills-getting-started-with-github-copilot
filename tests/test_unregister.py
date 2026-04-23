"""Tests for POST /activities/{activity_name}/unregister endpoint using AAA pattern"""

import pytest


@pytest.mark.parametrize("activity_name,email,expected_status,expected_message", [
    # Happy path - unregister existing participant
    ("Chess Club", "michael@mergington.edu", 200, "Unregistered michael@mergington.edu from Chess Club"),
    # Activity not found
    ("Nonexistent Activity", "test@example.com", 404, "Activity not found"),
    # Student not registered
    ("Basketball Team", "notregistered@example.com", 400, "Student is not registered for this activity"),
])
def test_unregister_scenarios(client, activity_name, email, expected_status, expected_message):
    """Test various unregister scenarios using AAA pattern"""
    # Arrange: Test client and test data provided via parametrize

    # Act: POST to unregister endpoint
    response = client.post(f"/activities/{activity_name}/unregister", params={"email": email})

    # Assert: Check status code and response message
    assert response.status_code == expected_status
    data = response.json()
    if expected_status == 200:
        assert data["message"] == expected_message
    else:
        assert data["detail"] == expected_message


def test_unregister_removes_participant(client):
    """Test that successful unregister removes participant from activity"""
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"

    # Verify participant is initially registered
    activities_response = client.get("/activities")
    activities_data = activities_response.json()
    assert email in activities_data[activity_name]["participants"]

    # Act
    response = client.post(f"/activities/{activity_name}/unregister", params={"email": email})

    # Assert
    assert response.status_code == 200
    # Verify participant was removed
    activities_response = client.get("/activities")
    activities_data = activities_response.json()
    assert email not in activities_data[activity_name]["participants"]