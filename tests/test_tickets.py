"""
Tests for /tickets endpoints.
"""
import pytest
from fastapi.testclient import TestClient
from tests.conftest import get_token


# ---------------------------------------------------------------------------
# POST /tickets
# ---------------------------------------------------------------------------
class TestCreateTicket:
    def test_create_ticket_as_customer(self, client: TestClient, customer_user):
        """Authenticated customer can create a ticket."""
        token = get_token(client, customer_user.email)
        response = client.post(
            "/tickets",
            json={
                "title": "My keyboard is broken",
                "description": "Keys are sticking after coffee spill.",
                "priority": "high",
            },
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 201
        body = response.json()
        assert body["title"] == "My keyboard is broken"
        assert body["status"] == "open"
        assert body["priority"] == "high"

    def test_create_ticket_as_agent(self, client: TestClient, agent_user):
        """Agents can also create tickets."""
        token = get_token(client, agent_user.email)
        response = client.post(
            "/tickets",
            json={
                "title": "Network outage on floor 3",
                "description": "Multiple users affected.",
                "priority": "medium",
            },
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 201

    def test_create_ticket_unauthenticated(self, client: TestClient):
        """Unauthenticated request returns 401."""
        response = client.post(
            "/tickets",
            json={"title": "No auth", "description": "Should fail.", "priority": "low"},
        )
        assert response.status_code == 401

    def test_create_ticket_missing_fields(self, client: TestClient, customer_user):
        """Missing required fields returns 422."""
        token = get_token(client, customer_user.email)
        response = client.post(
            "/tickets",
            json={"title": "Missing description"},
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 422


# ---------------------------------------------------------------------------
# GET /tickets
# ---------------------------------------------------------------------------
class TestListTickets:
    def test_list_tickets_as_customer(self, client: TestClient, customer_user, sample_ticket):
        """Customer sees only their own tickets."""
        token = get_token(client, customer_user.email)
        response = client.get("/tickets", headers={"Authorization": f"Bearer {token}"})
        assert response.status_code == 200
        body = response.json()
        assert isinstance(body, list)
        assert all(t["created_by"] == str(customer_user.id) for t in body)

    def test_list_tickets_as_admin(self, client: TestClient, admin_user, sample_ticket):
        """Admin sees all tickets."""
        token = get_token(client, admin_user.email)
        response = client.get("/tickets", headers={"Authorization": f"Bearer {token}"})
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_list_tickets_unauthenticated(self, client: TestClient):
        """Unauthenticated request returns 401."""
        response = client.get("/tickets")
        assert response.status_code == 401


# ---------------------------------------------------------------------------
# GET /tickets/{ticket_id}
# ---------------------------------------------------------------------------
class TestGetTicket:
    def test_get_ticket_owner(self, client: TestClient, customer_user, sample_ticket):
        """Ticket owner can fetch their ticket by ID."""
        token = get_token(client, customer_user.email)
        response = client.get(
            f"/tickets/{sample_ticket.id}",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 200
        assert response.json()["id"] == str(sample_ticket.id)

    def test_get_ticket_not_found(self, client: TestClient, admin_user):
        """Requesting a non-existent ticket ID returns 404."""
        import uuid
        token = get_token(client, admin_user.email)
        response = client.get(
            f"/tickets/{uuid.uuid4()}",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 404


# ---------------------------------------------------------------------------
# PATCH /tickets/{ticket_id}
# ---------------------------------------------------------------------------
class TestUpdateTicket:
    def test_update_status_as_agent(self, client: TestClient, agent_user, sample_ticket, admin_user):
        """Agent can update ticket status after being assigned to it."""
        # Admin atribui o ticket ao agent primeiro
        admin_token = get_token(client, admin_user.email)
        client.patch(
            f"/tickets/{sample_ticket.id}/assign",
            json={"agent_id": str(agent_user.id)},
            headers={"Authorization": f"Bearer {admin_token}"},
        )

        # Agora o agent pode atualizar
        token = get_token(client, agent_user.email)
        response = client.patch(
            f"/tickets/{sample_ticket.id}",
            json={"status": "in_progress"},
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 200
        assert response.json()["status"] == "in_progress"
    def test_update_status_as_admin(self, client: TestClient, admin_user, sample_ticket):
        """Admin can update ticket status."""
        token = get_token(client, admin_user.email)
        response = client.patch(
            f"/tickets/{sample_ticket.id}",
            json={"status": "in_progress"},
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 200
        assert response.json()["status"] == "in_progress"

    def test_update_unauthenticated(self, client: TestClient, sample_ticket):
        """Unauthenticated update returns 401."""
        response = client.patch(
            f"/tickets/{sample_ticket.id}",
            json={"status": "resolved"},
        )
        assert response.status_code == 401


# ---------------------------------------------------------------------------
# PATCH /tickets/{ticket_id}/assign
# ---------------------------------------------------------------------------
class TestAssignTicket:
    def test_assign_as_admin(self, client: TestClient, admin_user, agent_user, sample_ticket):
        """Admin can assign a ticket to an agent."""
        token = get_token(client, admin_user.email)
        response = client.patch(
            f"/tickets/{sample_ticket.id}/assign",
            json={"agent_id": str(agent_user.id)},
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 200
        assert response.json()["assigned_to"] == str(agent_user.id)

    def test_assign_as_agent(self, client: TestClient, agent_user, sample_ticket):
        """Agent can also assign tickets."""
        token = get_token(client, agent_user.email)
        response = client.patch(
            f"/tickets/{sample_ticket.id}/assign",
            json={"agent_id": str(agent_user.id)},
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 200

    def test_assign_as_customer_forbidden(self, client: TestClient, customer_user, agent_user, sample_ticket):
        """Customer cannot assign tickets — must return 403."""
        token = get_token(client, customer_user.email)
        response = client.patch(
            f"/tickets/{sample_ticket.id}/assign",
            json={"agent_id": str(agent_user.id)},
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 403
