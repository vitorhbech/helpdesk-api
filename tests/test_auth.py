"""
Tests for /auth/register and /auth/login endpoints.
"""
import pytest
from fastapi.testclient import TestClient


# ---------------------------------------------------------------------------
# POST /auth/register
# ---------------------------------------------------------------------------
class TestRegister:
    def test_register_success(self, client: TestClient):
        """New user can register and receives back their data."""
        response = client.post("/auth/register", json={
            "name": "Alice",
            "email": "alice@example.com",
            "password": "securepass123",
        })
        assert response.status_code == 201
        body = response.json()
        assert body["email"] == "alice@example.com"
        assert body["name"] == "Alice"
        assert body["role"] == "customer"          # default role
        assert "password" not in body              # password must never be returned
        assert "password_hash" not in body

    def test_register_duplicate_email(self, client: TestClient, customer_user):
        """Registering with an already-used email returns 400."""
        response = client.post("/auth/register", json={
            "name": "Duplicate",
            "email": customer_user.email,
            "password": "anypassword",
        })
        assert response.status_code == 400
        assert "already registered" in response.json()["detail"].lower()

    def test_register_missing_fields(self, client: TestClient):
        """Missing required fields returns 422 Unprocessable Entity."""
        response = client.post("/auth/register", json={"email": "incomplete@example.com"})
        assert response.status_code == 422


# ---------------------------------------------------------------------------
# POST /auth/login
# ---------------------------------------------------------------------------
class TestLogin:
    def test_login_success(self, client: TestClient, customer_user):
        """Valid credentials return an access token."""
        response = client.post("/auth/login", data={
            "username": customer_user.email,
            "password": "password123",
        })
        assert response.status_code == 200
        body = response.json()
        assert "access_token" in body
        assert body["token_type"] == "bearer"

    def test_login_wrong_password(self, client: TestClient, customer_user):
        """Wrong password returns 401."""
        response = client.post("/auth/login", data={
            "username": customer_user.email,
            "password": "wrongpassword",
        })
        assert response.status_code == 401
        assert "invalid credentials" in response.json()["detail"].lower()

    def test_login_unknown_email(self, client: TestClient):
        """Unknown email returns 401."""
        response = client.post("/auth/login", data={
            "username": "ghost@example.com",
            "password": "doesntmatter",
        })
        assert response.status_code == 401

    def test_login_missing_fields(self, client: TestClient):
        """Missing username/password returns 422."""
        response = client.post("/auth/login", data={"username": "only@email.com"})
        assert response.status_code == 422
