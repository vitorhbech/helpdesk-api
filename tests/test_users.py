"""
Tests for /users endpoints.
"""
import pytest
from fastapi.testclient import TestClient
from tests.conftest import get_token


# ---------------------------------------------------------------------------
# GET /users
# ---------------------------------------------------------------------------
class TestListUsers:
    def test_list_users_as_admin(self, client: TestClient, admin_user, customer_user, agent_user):
        """Admin can list all users in the system."""
        token = get_token(client, admin_user.email)
        response = client.get("/users", headers={"Authorization": f"Bearer {token}"})
        assert response.status_code == 200
        body = response.json()
        assert isinstance(body, list)
        assert len(body) >= 3  # at least the 3 users created in fixtures
        emails = [u["email"] for u in body]
        assert admin_user.email in emails
        assert customer_user.email in emails

    def test_list_users_as_customer_forbidden(self, client: TestClient, customer_user):
        """Customer cannot list users — must return 403."""
        token = get_token(client, customer_user.email)
        response = client.get("/users", headers={"Authorization": f"Bearer {token}"})
        assert response.status_code == 403

    def test_list_users_as_agent_forbidden(self, client: TestClient, agent_user):
        """Agent cannot list users — must return 403."""
        token = get_token(client, agent_user.email)
        response = client.get("/users", headers={"Authorization": f"Bearer {token}"})
        assert response.status_code == 403

    def test_list_users_unauthenticated(self, client: TestClient):
        """Unauthenticated request returns 401."""
        response = client.get("/users")
        assert response.status_code == 401


# ---------------------------------------------------------------------------
# PATCH /users/{user_id}/role
# ---------------------------------------------------------------------------
class TestChangeUserRole:
    def test_promote_customer_to_agent(self, client: TestClient, admin_user, customer_user):
        """Admin can promote a customer to agent."""
        token = get_token(client, admin_user.email)
        response = client.patch(
            f"/users/{customer_user.id}/role",
            json={"role": "agent"},
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 200
        assert response.json()["role"] == "agent"

    def test_demote_agent_to_customer(self, client: TestClient, admin_user, agent_user):
        """Admin can demote an agent back to customer."""
        token = get_token(client, admin_user.email)
        response = client.patch(
            f"/users/{agent_user.id}/role",
            json={"role": "customer"},
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 200
        assert response.json()["role"] == "customer"

    def test_change_role_as_customer_forbidden(self, client: TestClient, customer_user, agent_user):
        """Customer cannot change roles — must return 403."""
        token = get_token(client, customer_user.email)
        response = client.patch(
            f"/users/{agent_user.id}/role",
            json={"role": "admin"},
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 403

    def test_change_role_user_not_found(self, client: TestClient, admin_user):
        """Trying to change role of a non-existent user returns 404."""
        import uuid
        token = get_token(client, admin_user.email)
        response = client.patch(
            f"/users/{uuid.uuid4()}/role",
            json={"role": "agent"},
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 404

    def test_change_role_invalid_role(self, client: TestClient, admin_user, customer_user):
        """Passing an invalid role value returns 422."""
        token = get_token(client, admin_user.email)
        response = client.patch(
            f"/users/{customer_user.id}/role",
            json={"role": "superuser"},
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 400
