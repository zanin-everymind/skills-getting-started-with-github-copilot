from fastapi.testclient import TestClient
from src.app import app, activities

client = TestClient(app)


def test_get_activities():
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert "Chess Club" in data


def test_signup_and_unregister_flow():
    activity = "Chess Club"
    email = "pytest-test@example.com"

    # Ensure clean state
    if email in activities[activity]["participants"]:
        activities[activity]["participants"].remove(email)

    # Sign up
    r = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert r.status_code == 200
    assert email in activities[activity]["participants"]

    # Duplicate sign-up should fail
    r2 = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert r2.status_code == 400

    # Unregister
    r3 = client.post(f"/activities/{activity}/unregister", params={"email": email})
    assert r3.status_code == 200
    assert email not in activities[activity]["participants"]

    # Unregistering again should return 404
    r4 = client.post(f"/activities/{activity}/unregister", params={"email": email})
    assert r4.status_code == 404
