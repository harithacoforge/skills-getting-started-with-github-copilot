import pytest
import copy
from fastapi.testclient import TestClient

from src.app import app, activities


@pytest.fixture
def client():
    """Test client for FastAPI app"""
    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_activities():
    """Reset activities data after each test to ensure clean state"""
    original_activities = copy.deepcopy(activities)
    yield
    activities.clear()
    activities.update(original_activities)