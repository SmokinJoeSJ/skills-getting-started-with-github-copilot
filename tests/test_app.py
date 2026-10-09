from fastapi.testclient import TestClient

from src.app import app, activities


client = TestClient(app)


def test_signup_rejects_duplicate_registration():
    original = activities["Chess Club"]["participants"][:]
    try:
        response = client.post("/activities/Chess%20Club/signup?email=michael@mergington.edu")

        assert response.status_code == 400
        assert response.json()["detail"] == "Student already signed up for this activity"
    finally:
        activities["Chess Club"]["participants"] = original


def test_unregister_removes_participant():
    original = activities["Chess Club"]["participants"][:]
    try:
        activities["Chess Club"]["participants"] = [
            "michael@mergington.edu",
            "daniel@mergington.edu",
        ]

        response = client.delete("/activities/Chess%20Club/unregister?email=michael@mergington.edu")

        assert response.status_code == 200
        assert "michael@mergington.edu" not in activities["Chess Club"]["participants"]
        assert response.json()["message"] == "Removed michael@mergington.edu from Chess Club"
    finally:
        activities["Chess Club"]["participants"] = original
