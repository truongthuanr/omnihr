from sqlalchemy import text
from typing import Optional
from sqlalchemy.orm import Session

class OrganizationRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_organization_id_by_api_key(self, api_key: str) -> Optional[int]:
        result = self.db.execute(
            text("SELECT organization_id FROM org_api_keys WHERE api_key = :key"),
            {"key": api_key}
        ).fetchone()
        return result[0] if result else None
