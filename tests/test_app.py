from fastapi.testclient import TestClient

from src.app import app


client = TestClient(app)


def test_get_activities_returns_the_expected_activity_names():
    response = client.get("/activities")

    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert "Programming Class" in data
    assert "Gym Class" in data


def test_signup_for_activity_success():
    email = "new-student@mergington.edu"
    activity_name = "Chess Club"

    client.delete(f"/activities/{activity_name}/unregister?email={email}")

    response = client.post(f"/activities/{activity_name}/signup?email={email}")

    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {email} for {activity_name}"}

    activities = client.get("/activities").json()
    assert email in activities[activity_name]["participants"]

    client.delete(f"/activities/{activity_name}/unregister?email={email}")


def test_signup_rejects_duplicate_registration():
    email = "duplicate-test@mergington.edu"
    activity_name = "Chess Club"

    client.delete(f"/activities/{activity_name}/unregister?email={email}")

    first_response = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert first_response.status_code == 200

    duplicate_response = client.post(f"/activities/{activity_name}/signup?email={email}")

    assert duplicate_response.status_code == 400
    assert duplicate_response.json()["detail"] == "Student is already signed up for this activity"

    client.delete(f"/activities/{activity_name}/unregister?email={email}")


def test_unregister_removes_participant_from_activity():
    email = "unregister-test@mergington.edu"
    activity_name = "Chess Club"

    client.post(f"/activities/{activity_name}/signup?email={email}")

    response = client.delete(f"/activities/{activity_name}/unregister?email={email}")

    assert response.status_code == 200
    assert response.json() == {"message": f"Removed {email} from {activity_name}"}

    activity_response = client.get("/activities")
    assert email not in activity_response.json()[activity_name]["participants"]


def test_signup_for_nonexistent_activity():
    response = client.post("/activities/Does Not Exist/signup?email=test@mergington.edu")

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_for_nonexistent_activity():
    response = client.delete("/activities/Does Not Exist/unregister?email=test@mergington.edu")

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
