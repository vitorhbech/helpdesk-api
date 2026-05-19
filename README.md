# Helpdesk API

A RESTful API for helpdesk ticket management, built with **FastAPI**, **PostgreSQL**, **SQLAlchemy**, and **Alembic**. Supports user authentication with JWT, role-based access control, and full ticket lifecycle management.

---

## Features

- **Authentication** — User registration and login with JWT tokens
- **Role-based access control** — Separate permissions for admins and regular users
- **Ticket management** — Create, update, and track support tickets
- **Status updates** — Move tickets through their lifecycle (e.g., open → in progress → resolved)
- **Ticket assignment** — Assign tickets to specific users/agents
- **Database migrations** — Schema versioning with Alembic

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

---

## Prerequisites

- Python 3.10+
- PostgreSQL running locally

---

## Getting Started

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

Create a `.env` file in the root directory:

```env
DATABASE_URL=postgresql://your_user:your_password@localhost:5432/helpdesk_db
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 5. Run database migrations

```bash
alembic upgrade head
```

### 6. Start the server

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`.

Interactive docs (Swagger UI) at `http://localhost:8000/docs`.

---

## API Overview

| Method | Endpoint | Description | Auth required |
|---|---|---|---|
| POST | `/auth/register` | Register a new user | No |
| POST | `/auth/login` | Login and get JWT token | No |
| GET | `/tickets` | List all tickets | Yes |
| POST | `/tickets` | Create a new ticket | Yes |
| PATCH | `/tickets/{id}/status` | Update ticket status | Yes (admin) |
| PATCH | `/tickets/{id}/assign` | Assign ticket to a user | Yes (admin) |

> Full interactive documentation available at `/docs` after running the server.

---

## Project Structure

```
helpdesk-api/
├── app/
│   ├── api/
│   │   └── routes/      # API route handlers
│   ├── core/            # Settings and configuration
│   ├── models/          # SQLAlchemy models
│   ├── schemas/         # Pydantic schemas
│   └── services/        # Business logic layer
├── alembic/
│   └── versions/        # Migration files
├── tests/               # Test suite
├── alembic.ini
└── requirements.txt
```

---

##                                                 License

This project is for educational purposes.
