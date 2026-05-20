import uuid
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.api.deps import get_db
from app.models.database import Base
from app.models.user import User
from app.models.ticket import Ticket
from app.core.security import hash_password
import os 
from dotenv import load_dotenv

# ---------------------------------------------------------------------------
# Test database — uses a separate PostgreSQL DB so tests never touch production
# ---------------------------------------------------------------------------
load_dotenv()

_prod_url = os.getenv("DATABASE_URL", "")
TEST_DATABASE_URL = _prod_url.rsplit("/", 1)[0] + "/helpdesk_test"

engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# ---------------------------------------------------------------------------
# Create all tables once per test session, drop them at the end
# ---------------------------------------------------------------------------
@pytest.fixture(scope="session", autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


# ---------------------------------------------------------------------------
# Each test gets its own DB session wrapped in a transaction that is rolled
# back at the end — so tests are fully isolated without recreating tables.
# ---------------------------------------------------------------------------
@pytest.fixture
def db():
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()


# ---------------------------------------------------------------------------
# TestClient that overrides get_db to use the test session
# ---------------------------------------------------------------------------
@pytest.fixture
def client(db):
    def override_get_db():
        yield db

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


# ---------------------------------------------------------------------------
# User fixtures
# ---------------------------------------------------------------------------
@pytest.fixture
def customer_user(db):
    user = User(
        id=uuid.uuid4(),
        name="Test Customer",
        email="customer@test.com",
        password_hash=hash_password("password123"),
        role="customer",
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@pytest.fixture
def agent_user(db):
    user = User(
        id=uuid.uuid4(),
        name="Test Agent",
        email="agent@test.com",
        password_hash=hash_password("password123"),
        role="agent",
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@pytest.fixture
def admin_user(db):
    user = User(
        id=uuid.uuid4(),
        name="Test Admin",
        email="admin@test.com",
        password_hash=hash_password("password123"),
        role="admin",
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


# ---------------------------------------------------------------------------
# Helper — returns a Bearer token for a given user
# ---------------------------------------------------------------------------
def get_token(client: TestClient, email: str, password: str = "password123") -> str:
    response = client.post("/auth/login", data={"username": email, "password": password})
    assert response.status_code == 200, f"Login failed for {email}: {response.json()}"
    return response.json()["access_token"]


# ---------------------------------------------------------------------------
# Ticket fixture (customer-owned, unassigned)
# ---------------------------------------------------------------------------
@pytest.fixture
def sample_ticket(db, customer_user):
    ticket = Ticket(
        id=uuid.uuid4(),
        title="Printer not working",
        description="The office printer on floor 2 is offline.",
        status="open",
        priority="medium",
        created_by=customer_user.id,
    )
    db.add(ticket)
    db.commit()
    db.refresh(ticket)
    return ticket
