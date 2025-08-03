# api/employee_router.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.schemas.employee_schema import EmployeeRead
from app.services.employee_service import search_employees_service
from app.core.database import get_db
from app.api.employee_param import EmployeeSearchParams

router = APIRouter()

@router.get("/employees/search", response_model=List[EmployeeRead])
def search_employees(
    params: EmployeeSearchParams = Depends(),
    db: Session = Depends(get_db)
):
    return search_employees_service(params, db)
