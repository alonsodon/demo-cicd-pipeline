import pytest
from app.main import app


@pytest.fixture
def client():
    """Crea un cliente de test de Flask. La app no arranca un servidor real."""
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


class TestHealth:
    def test_health_returns_200(self, client):
        response = client.get("/health")
        assert response.status_code == 200

    def test_health_returns_ok_status(self, client):
        data = client.get("/health").get_json()
        assert data["status"] == "ok"
        assert "uptime_seconds" in data


class TestGreet:
    def test_greet_known_name(self, client):
        response = client.get("/greet/Mike")
        assert response.status_code == 200
        assert response.get_json()["message"] == "Hello, Mike!"

    def test_greet_returns_name_field(self, client):
        response = client.get("/greet/Thomas")
        assert response.get_json()["name"] == "Thomas"


class TestEcho:
    def test_echo_returns_same_data(self, client):
        payload = {"key": "value", "number": 42}
        response = client.post("/echo", json=payload)
        assert response.status_code == 200
        assert response.get_json()["echo"] == payload

    def test_echo_rejects_non_json(self, client):
        response = client.post("/echo", data="not json", content_type="text/plain")
        assert response.status_code == 400
