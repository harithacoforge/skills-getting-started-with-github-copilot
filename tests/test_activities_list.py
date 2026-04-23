"""Tests for GET /activities endpoint using AAA pattern"""

import pytest


def test_get_activities_success(client):
    """Test successful retrieval of all activities"""
    # Arrange: Test client is provided via fixture

    # Act: Call the GET /activities endpoint
    response = client.get("/activities")

    # Assert: Check status code and response structure
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert len(data) == 9  # Based on the app's activities

    # Verify structure of first activity
    chess_club = data["Chess Club"]
    assert "description" in chess_club
    assert "schedule" in chess_club
    assert "max_participants" in chess_club
    assert "participants" in chess_club
    assert isinstance(chess_club["participants"], list)