import pytest
from app import create_app


@pytest.fixture()
def client():
    app = create_app({
        "TESTING": True,
        "API_KEY": "test-secret-key"
    })
    with app.test_client() as test_client:
        yield test_client


def auth_headers():
    return {"X-API-Key": "test-secret-key"}


def test_health_endpoint_is_public(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json()["success"] is True


def test_protected_endpoint_rejects_missing_api_key(client):
    response = client.get("/api/tasks")
    assert response.status_code == 401
    assert response.get_json()["success"] is False


def test_create_task_successfully(client):
    response = client.post(
        "/api/tasks",
        json={"title": "Complete SWYNEX Task 3", "description": "Test the API"},
        headers=auth_headers()
    )
    assert response.status_code == 201
    assert response.get_json()["data"]["title"] == "Complete SWYNEX Task 3"


def test_create_task_rejects_empty_title(client):
    response = client.post(
        "/api/tasks",
        json={"title": "   "},
        headers=auth_headers()
    )
    assert response.status_code == 400
    assert "title" in response.get_json()["error"]["details"]


def test_get_tasks(client):
    client.post(
        "/api/tasks",
        json={"title": "First task"},
        headers=auth_headers()
    )
    response = client.get("/api/tasks", headers=auth_headers())
    assert response.status_code == 200
    assert response.get_json()["count"] == 1


def test_task_not_found(client):
    response = client.get("/api/tasks/999", headers=auth_headers())
    assert response.status_code == 404
