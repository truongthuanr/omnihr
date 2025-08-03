from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional, List
from schemas.employee import EmployeeRead
from services.employee import search_employees_service
from database import get_db

router = APIRouter()


class EmployeeSearchParams:
    def __init__(
        self,
        status_id: Optional[int] = Query(None),
        location_id: Optional[int] = Query(None),
        department_id: Optional[int] = Query(None),
        position_id: Optional[int] = Query(None),
        company_id: Optional[int] = Query(None),
        page: int = Query(1, ge=1),
        size: int = Query(20, ge=1, le=100)
    ):
        self.status_id = status_id
        self.location_id = location_id
        self.department_id = department_id
        self.position_id = position_id
        self.company_id = company_id
        self.page = page
        self.size = size


@router.get("/employees/search", response_model=List[EmployeeRead])
def search_employees(
    params: EmployeeSearchParams = Depends(),
    db: Session = Depends(get_db)
):
    return search_employees_service(params, db)
