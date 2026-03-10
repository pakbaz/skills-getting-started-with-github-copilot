import copy
import pytest
from fastapi.testclient import TestClient
from src.app import app, activities

@pytest.fixture(autouse=True)
def reset_activities():
    """Reset the in-memory activities to their original state before each test."""
    original = copy.deepcopy(activities)
    yield
    activities.clear()
    activities.update(original)


client = TestClient(app)


# ── GET / ────────────────────────────────────────────────────────────────────

def test_root_redirects():
    # Arrange: nothing extra needed

    # Act
    response = client.get("/", follow_redirects=False)

    # Assert
    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"


# ── GET /activities ──────────────────────────────────────────────────────────

def test_get_activities_returns_all():
    # Arrange: default activities are loaded via the fixture

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert "Gym Class" in data
    assert "Soccer Team" in data


def test_get_activities_structure():
    # Arrange: default activities are loaded via the fixture

    # Act
    response = client.get("/activities")
    data = response.json()

    # Assert
    for name, details in data.items():
        assert "description" in details
        assert "schedule" in details
        assert "max_participants" in details
        assert "participants" in details
        assert isinstance(details["participants"], list)


# ── POST /activities/{name}/signup ───────────────────────────────────────────

def test_signup_success():
    # Arrange
    email = "test@mergington.edu"
    activity_name = "Chess Club"

    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={email}")

    # Assert
    assert response.status_code == 200
    assert email in response.json()["message"]
    updated = client.get("/activities").json()
    assert email in updated[activity_name]["participants"]


def test_signup_nonexistent_activity():
    # Arrange
    email = "test@mergington.edu"
    activity_name = "Nonexistent"

    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={email}")

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_signup_adds_to_participants_list():
    # Arrange
    email = "new@mergington.edu"
    activity_name = "Chess Club"
    participants_before = client.get("/activities").json()[activity_name]["participants"][:]

    # Act
    client.post(f"/activities/{activity_name}/signup?email={email}")

    # Assert
    participants_after = client.get("/activities").json()[activity_name]["participants"]
    assert len(participants_after) == len(participants_before) + 1
    assert email in participants_after


# ── DELETE /activities/{name}/signup ─────────────────────────────────────────

def test_unregister_success():
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"  # default Chess Club participant

    # Act
    response = client.delete(f"/activities/{activity_name}/signup?email={email}")

    # Assert
    assert response.status_code == 200
    assert email in response.json()["message"]
    updated = client.get("/activities").json()
    assert email not in updated[activity_name]["participants"]


def test_unregister_nonexistent_activity():
    # Arrange
    email = "test@mergington.edu"
    activity_name = "Nonexistent"

    # Act
    response = client.delete(f"/activities/{activity_name}/signup?email={email}")

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_student_not_in_activity():
    # Arrange
    email = "nobody@mergington.edu"
    activity_name = "Chess Club"

    # Act
    response = client.delete(f"/activities/{activity_name}/signup?email={email}")

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Student not found in activity"


def test_unregister_removes_from_participants_list():
    # Arrange
    activity_name = "Chess Club"
    participants_before = client.get("/activities").json()[activity_name]["participants"][:]
    email = participants_before[0]

    # Act
    client.delete(f"/activities/{activity_name}/signup?email={email}")

    # Assert
    participants_after = client.get("/activities").json()[activity_name]["participants"]
    assert len(participants_after) == len(participants_before) - 1
    assert email not in participants_after


# ── Signup + Unregister round-trip ───────────────────────────────────────────

def test_signup_then_unregister():
    # Arrange
    email = "roundtrip@mergington.edu"
    activity_name = "Gym Class"

    # Act: sign up
    client.post(f"/activities/{activity_name}/signup?email={email}")

    # Assert: participant is present
    participants = client.get("/activities").json()[activity_name]["participants"]
    assert email in participants

    # Act: unregister
    client.delete(f"/activities/{activity_name}/signup?email={email}")

    # Assert: participant is removed
    participants = client.get("/activities").json()[activity_name]["participants"]
    assert email not in participants
