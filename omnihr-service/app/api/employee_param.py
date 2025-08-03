# api/employee_param.py
from pydantic import BaseModel
from typing import Optional
from fastapi import Query

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

