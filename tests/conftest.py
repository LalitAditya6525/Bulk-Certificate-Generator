import os

# Set these before importing the application/database modules.
os.environ["DATABASE_URL"] = "sqlite:///./test_bulk_certificates.db"
os.environ["CERTIFICATE_DIR"] = "tests/test_generated"

import pytest
from fastapi.testclient import TestClient

from app.database import Base, engine
from app.main import app


@pytest.fixture
def client():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    with TestClient(app) as test_client:
        yield test_client

    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def sample_payload():
    return {
        "course_name": "Python Programming",
        "certificate_date": "2026-10-10",
        "recipients": [
            {
                "name": "Aditya Kumar",
                "email": "aditya@example.com",
            },
            {
                "name": "Priya Sharma",
                "email": "priya@example.com",
            },
        ],
    }
