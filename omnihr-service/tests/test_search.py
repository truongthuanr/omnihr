import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

os.environ["CONFIG_PATH"] = os.path.join(os.path.dirname(__file__), "test_config.json")

from app.main import app
from app.models.model import (
    Base, Employee, Department, Position, Status,
    Company, Location, Organization, OrgApiKey
)
from app.core.database import get_db

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

ORG_KEY = "test-org-key"

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

@pytest.fixture(scope="module", autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()

    # Tạo organization và api key
    org = Organization(id=1, name="TestOrg")
    db.add(org)
    db.flush()  # để đảm bảo org.id có giá trị

    db.add(OrgApiKey(api_key=ORG_KEY, organization_id=org.id, description="Test Key"))

    # Reference data
    db.add_all([
        Department(id=1, name="Engineering"),
        Department(id=2, name="HR"),
        Position(id=1, name="Backend Engineer"),
        Position(id=2, name="Product Manager"),
        Location(id=1, name="Hanoi"),
        Location(id=2, name="HCM"),
        Company(id=1, name="Zeta Inc"),
        Status(id=1, name="Active"),
        Status(id=2, name="Not Started")
    ])

    db.add_all([
        Employee(
            first_name="John", last_name="Doe", contact="john@example.com",
            department_id=1, position_id=1, location_id=1,
            status_id=1, company_id=1, organization_id=org.id,
            internal_note="Internal test employee"
        ),
        Employee(
            first_name="Jane", last_name="Smith", contact="jane@example.com",
            department_id=2, position_id=2, location_id=2,
            status_id=1, company_id=1, organization_id=org.id,
            internal_note="Another note"
        )
    ])

    db.commit()
    db.close()
    yield
    Base.metadata.drop_all(bind=engine)


def test_search_employees_with_filters():
    response = client.get(
        "/employees/search",
        params={"department_id": 1, "page": 1, "size": 10},
        headers={"X-org-key": ORG_KEY}
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["first_name"] == "John"
    assert data[0]["department"] == "Engineering"


def test_search_employees_pagination():
    response = client.get(
        "/employees/search?page=1&size=1",
        headers={"X-org-key": ORG_KEY}
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 1


def test_search_employees_empty_result():
    response = client.get(
        "/employees/search?department_id=999",
        headers={"X-org-key": ORG_KEY}
    )
    assert response.status_code == 200
    assert response.json() == []





def test_missing_org_key():
    response = client.get("/employees/search")
    assert response.status_code == 422
    assert "X-ORG-KEY" in response.text



def test_invalid_org_key():
    response = client.get(
        "/employees/search",
        headers={"X-org-key": "invalid-key"}
    )
    assert response.status_code == 403
    assert "Invalid organization key" in response.text


def test_rate_limit_exceeded():
    for _ in range(61):  # giả định max_requests = 10
        response = client.get(
            "/employees/search",
            headers={"X-org-key": ORG_KEY}
        )
    assert response.status_code == 429
