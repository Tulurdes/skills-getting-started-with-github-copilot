from fastapi.testclient import TestClient

from src.app import app


client = TestClient(app)


def test_unregister_removes_participant_from_activity():
    email = "unregister-test@mergington.edu"
    client.post(f"/activities/Chess Club/signup?email={email}")

    response = client.delete(f"/activities/Chess Club/unregister?email={email}")

    assert response.status_code == 200
    assert response.json() == {"message": f"Removed {email} from Chess Club"}

    activity_response = client.get("/activities")
    assert email not in activity_response.json()["Chess Club"]["participants"]


def test_signup_rejects_duplicate_registration():
    email = "duplicate-test@mergington.edu"
    client.delete(f"/activities/Chess Club/unregister?email={email}")

    response = client.post(f"/activities/Chess Club/signup?email={email}")
    assert response.status_code == 200

    duplicate_response = client.post(f"/activities/Chess Club/signup?email={email}")
    assert duplicate_response.status_code == 400
    assert duplicate_response.json()["detail"] == "Student is already signed up for this activity"

    client.delete(f"/activities/Chess Club/unregister?email={email}")
