from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)


def test_get_activities_returns_activity_data():
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)
    # basic sanity checks
    assert "Chess Club" in data
    assert isinstance(data["Chess Club"]["participants"], list)


def test_signup_and_remove_flow():
    email = "tester_ci@example.com"

    # signup
    resp = client.post(f"/activities/Chess Club/signup?email={email}")
    assert resp.status_code == 200
    assert "Signed up" in resp.json().get("message", "")

    # duplicate signup should return 400
    resp_dup = client.post(f"/activities/Chess Club/signup?email={email}")
    assert resp_dup.status_code == 400

    # participant should appear in the activity list
    resp_list = client.get("/activities")
    assert email in resp_list.json()["Chess Club"]["participants"]

    # remove participant
    resp_remove = client.delete(f"/activities/Chess Club/participants?email={email}")
    assert resp_remove.status_code == 200

    # removing again should return 404
    resp_remove_again = client.delete(f"/activities/Chess Club/participants?email={email}")
    assert resp_remove_again.status_code == 404
