from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.models.model import Employee
from typing import List, Optional


class EmployeeRepository:
    def __init__(self, db: Session):
        self.db = db

    def get(self, employee_id: int) -> Optional[Employee]:
        return self.db.query(Employee).filter(Employee.id == employee_id).first()

    def list(self, skip: int = 0, limit: int = 100) -> List[Employee]:
        return self.db.query(Employee).offset(skip).limit(limit).all()

    def create(self, employee_data: dict) -> Employee:
        employee = Employee(**employee_data)
        self.db.add(employee)
        self.db.commit()
        self.db.refresh(employee)
        return employee

    def update(self, employee_id: int, update_data: dict) -> Optional[Employee]:
        employee = self.get(employee_id)
        if not employee:
            return None

        for key, value in update_data.items():
            setattr(employee, key, value)

        self.db.commit()
        self.db.refresh(employee)
        return employee

    def delete(self, employee_id: int) -> bool:
        employee = self.get(employee_id)
        if not employee:
            return False

        self.db.delete(employee)
        self.db.commit()
        return True

from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import List, Optional
from app.models.model import Employee

class EmployeeRepository:
    def __init__(self, db: Session):
        self.db = db

    def search(
        self,
        filters: dict,
        skip: int = 0,
        limit: int = 100
    ) -> List[Employee]:
        query = self.db.query(Employee)

        if company_id := filters.get("company_id"):
            query = query.filter(Employee.company_id == company_id)
        if department_id := filters.get("department_id"):
            query = query.filter(Employee.department_id == department_id)
        if position_id := filters.get("position_id"):
            query = query.filter(Employee.position_id == position_id)
        if location_id := filters.get("location_id"):
            query = query.filter(Employee.location_id == location_id)
        if status_id := filters.get("status_id"):
            query = query.filter(Employee.status_id == status_id)

        return query.offset(skip).limit(limit).all()

