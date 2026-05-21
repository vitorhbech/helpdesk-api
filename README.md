# Helpdesk API
![Tests](https://github.com/vitorhbech/helpdesk-api/actions/workflows/tests.yml/badge.svg)

A RESTful API for helpdesk ticket management, built with **FastAPI**, **PostgreSQL**, **SQLAlchemy**, and **Alembic**. Supports user authentication with JWT, role-based access control, and a full ticket lifecycle workflow.

---

## Features

- **Authentication** — User registration and login with JWT tokens
- **Role-based access control** — Separate permissions for admin, agent, and customer roles
- **Ticket management** — Create, update, and track support tickets
- **Status workflow** — Structured lifecycle: `open → in_progress → resolved → closed`
- **Ticket assignment** — Assign tickets to specific agents
- **Database migrations** — Schema versioning with Alembic
- **Automated tests** — 31 tests covering auth, tickets, and user management
- **Docker support** — Full containerized environment with Docker Compose

---

## Tech Stack

| Layer | Technology |
|---|---|
| Framework | FastAPI |
| Database | PostgreSQL |
| ORM | SQLAlchemy 2.0 |
| Migrations | Alembic |
| Validation | Pydantic v2 |
| Auth | JWT (python-jose + passlib + bcrypt) |
| Server | Uvicorn |
| Containers | Docker + Docker Compose |
| Tests | pytest + httpx |

---

## API Overview

| Method | Endpoint | Description | Auth required |
|---|---|---|---|
| POST | `/auth/register` | Register a new user | No |
| POST | `/auth/login` | Login and get JWT token | No |
| GET | `/tickets` | List tickets | Yes |
| POST | `/tickets` | Create a new ticket | Yes |
| GET | `/tickets/{id}` | Get ticket details | Yes |
| PATCH | `/tickets/{id}` | Update ticket status | Yes |
| PATCH | `/tickets/{id}/assign` | Assign ticket to an agent | Yes (admin/agent) |
| GET | `/users` | List all users | Yes (admin) |
| PATCH | `/users/{id}/role` | Update a user's role | Yes (admin) |
| GET | `/health` | Health check | No |

> Full interactive documentation available at `http://localhost:8000/docs` after running the server.

---

## Running with Docker (recommended)

### Prerequisites
- [Docker Desktop](https://www.docker.com/products/docker-desktop)

### 1. Clone the repository

```bash
git clone https://github.com/vitorhbech/helpdesk-api.git
cd helpdesk-api
```

### 2. Set up environment variables

```bash
cp .env.example .env
```

Then open `.env` and update the values accordingly.

### 3. Start the containers

```bash
docker compose up --build
```

### 4. Run database migrations

In a separate terminal:

```bash
docker compose exec api alembic upgrade head
```

The API will be available at `http://localhost:8000`.

---

## Running Locally

### Prerequisites
- Python 3.10+
- PostgreSQL running locally

### 1. Clone the repository

```bash
git clone https://github.com/vitorhbech/helpdesk-api.git
cd helpdesk-api
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up environment variables

```bash
cp .env.example .env
```

Then open `.env` and update the values accordingly.

### 5. Run database migrations

```bash
alembic upgrade head
```

### 6. Start the server

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`.

---

## Running Tests

Create a dedicated test database:

```bash
psql -U postgres -c "CREATE DATABASE helpdesk_test;"
```

Run the full test suite:

```bash
pytest -v
```

See [`tests/README.md`](tests/README.md) for full test documentation.

---

## Project Structure

```
helpdesk-api/
├── app/
│   ├── api/
│   │   └── routes/      # API route handlers
│   ├── core/            # Settings and security
│   ├── models/          # SQLAlchemy models
│   ├── schemas/         # Pydantic schemas
│   └── services/        # Business logic layer
├── alembic/
│   └── versions/        # Migration files
├── tests/               # Automated test suite
├── Dockerfile
├── docker-compose.yml
├── alembic.ini
└── requirements.txt
```

---

## License

This project is for educational purposes.