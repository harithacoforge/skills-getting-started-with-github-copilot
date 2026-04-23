"""Tests for GET / redirect endpoint using AAA pattern"""

import pytest


def test_root_redirect(client):
    """Test that root endpoint redirects to static HTML"""
    # Arrange: Test client provided via fixture

    # Act: GET request to root
    response = client.get("/", follow_redirects=False)  # Don't follow redirect

    # Assert: Check redirect status and location
    assert response.status_code == 307  # Temporary Redirect
    assert response.headers["location"] == "/static/index.html"