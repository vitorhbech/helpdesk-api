# Tests

This directory contains the automated test suite for the Helpdesk API. Tests are written with **pytest** and use a dedicated PostgreSQL database to run in full isolation from the development environment.

---

## Requirements

- Python 3.10+
- PostgreSQL running locally
- Dependencies installed (`pip install -r requirements.txt`)
- A `.env` file configured at the project root (see main README)

Install test dependencies:

```bash
pip install pytest httpx
```

---

## Setup

Create a dedicated test database (only needed once):

```bash
psql -U postgres -c "CREATE DATABASE helpdesk_test;"
```

The test suite automatically creates and drops all tables — no manual migrations needed.

---

## Running the tests

Run the full test suite from the **project root**:

```bash
pytest
```

With verbose output (recommended):

```bash
pytest -v
```

Save output to a file:

```bash
pytest -v > test_results.txt
```

Run a specific file:

```bash
pytest tests/test_auth.py -v
```

Run a specific test:

```bash
pytest tests/test_auth.py::TestLogin::test_login_success -v
```

---

## Test structure

```
tests/
├── conftest.py        # Database setup, shared fixtures, helper functions
├── test_auth.py       # Authentication endpoints
├── test_tickets.py    # Ticket management endpoints
└── test_users.py      # User management endpoints
```

---

## What is being tested

### `test_auth.py` — Authentication
| Test | Description |
|---|---|
| `test_register_success` | New user registers and receives correct data back |
| `test_register_duplicate_email` | Duplicate email returns 400 |
| `test_register_missing_fields` | Incomplete payload returns 422 |
| `test_login_success` | Valid credentials return a JWT token |
| `test_login_wrong_password` | Wrong password returns 401 |
| `test_login_unknown_email` | Unknown email returns 401 |
| `test_login_missing_fields` | Missing fields return 422 |

### `test_tickets.py` — Ticket Management
| Test | Description |
|---|---|
| `test_create_ticket_as_customer` | Customer creates a ticket successfully |
| `test_create_ticket_as_agent` | Agent creates a ticket successfully |
| `test_create_ticket_unauthenticated` | Unauthenticated request returns 401 |
| `test_create_ticket_missing_fields` | Incomplete payload returns 422 |
| `test_list_tickets_as_customer` | Customer sees only their own tickets |
| `test_list_tickets_as_admin` | Admin sees all tickets |
| `test_list_tickets_unauthenticated` | Unauthenticated request returns 401 |
| `test_get_ticket_owner` | Ticket owner can fetch their ticket by ID |
| `test_get_ticket_not_found` | Non-existent ticket ID returns 404 |
| `test_update_status_as_agent` | Agent updates ticket status after being assigned |
| `test_update_status_as_admin` | Admin updates ticket status |
| `test_update_unauthenticated` | Unauthenticated update returns 401 |
| `test_assign_as_admin` | Admin assigns a ticket to an agent |
| `test_assign_as_agent` | Agent assigns a ticket to themselves |
| `test_assign_as_customer_forbidden` | Customer cannot assign tickets — returns 403 |

### `test_users.py` — User Management
| Test | Description |
|---|---|
| `test_list_users_as_admin` | Admin lists all users in the system |
| `test_list_users_as_customer_forbidden` | Customer cannot list users — returns 403 |
| `test_list_users_as_agent_forbidden` | Agent cannot list users — returns 403 |
| `test_list_users_unauthenticated` | Unauthenticated request returns 401 |
| `test_promote_customer_to_agent` | Admin promotes a customer to agent |
| `test_demote_agent_to_customer` | Admin demotes an agent to customer |
| `test_change_role_as_customer_forbidden` | Customer cannot change roles — returns 403 |
| `test_change_role_user_not_found` | Non-existent user ID returns 404 |
| `test_change_role_invalid_role` | Invalid role value returns 400 |

---

## Test isolation

Each test runs inside a database transaction that is **rolled back** at the end, so tests never affect each other. The test database is fully independent from the development database.
