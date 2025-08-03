from sqlalchemy.orm import Session
from app.models.model import Employee
from typing import List, Optional


def get_employee(db: Session, employee_id: int) -> Optional[Employee]:
    return db.query(Employee).filter(Employee.id == employee_id).first()


def get_employees(
    db: Session,
    skip: int = 0,
    limit: int = 100
) -> List[Employee]:
    return db.query(Employee).offset(skip).limit(limit).all()


def create_employee(db: Session, employee_data: dict) -> Employee:
    employee = Employee(**employee_data)
    db.add(employee)
    db.commit()
    db.refresh(employee)
    return employee


def update_employee(db: Session, employee_id: int, update_data: dict) -> Optional[Employee]:
    employee = get_employee(db, employee_id)
    if not employee:
        return None

    for key, value in update_data.items():
        setattr(employee, key, value)

    db.commit()
    db.refresh(employee)
    return employee


def delete_employee(db: Session, employee_id: int) -> bool:
    employee = get_employee(db, employee_id)
    if not employee:
        return False

    db.delete(employee)
    db.commit()
    return True
