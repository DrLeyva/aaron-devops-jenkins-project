from app import app


def test_home_endpoint():
    client = app.test_client()

    response = client.get("/")
    data = response.get_json()

    assert response.status_code == 200
    assert data["application"] == "Aaron DevOps Project"
    assert data["version"] == "1.0.0"


def test_health_endpoint():
    client = app.test_client()

    response = client.get("/health")
    data = response.get_json()

    assert response.status_code == 200
    assert data["status"] == "healthy"