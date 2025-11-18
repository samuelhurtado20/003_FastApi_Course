import os
import sys
from pathlib import Path

from sqlalchemy import create_engine
from sqlmodel import SQLModel, Session
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.pool import StaticPool

# 👇 AÑADIR LA RAÍZ DEL PROYECTO AL sys.path
BASE_DIR = Path(__file__).resolve().parents[2]
if str(BASE_DIR) not in sys.path:
    sys.path.append(str(BASE_DIR))

from app.main import app  # 👈 ahora sí funciona
from app.db.db2 import get_session


# Get the test database URL from environment variables
DATABASE_URL_TEST = os.getenv("DATABASE_URL_TEST")

if not DATABASE_URL_TEST:
    raise ValueError("DATABASE_URL_TEST no está definido en el entorno")

# Create the test engine with StaticPool to maintain the same connection
engine = create_engine(
    DATABASE_URL_TEST,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)


@pytest.fixture(name="session")
def fixture_session():
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session
    SQLModel.metadata.drop_all(engine)


@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        yield session

    app.dependency_overrides[get_session] = get_session_override
    yield TestClient(app)
    app.dependency_overrides.clear()
