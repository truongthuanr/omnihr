from sqlalchemy.orm import Session
from fastapi import HTTPException
from sqlalchemy import func, or_
from typing import Any

from app.repositories.employee_repository import EmployeeRepository
from app.repositories.origanization_repository import OrganizationRepository
from app.models.model import Employee
from app.config.config import config
from app.api.employee_param import EmployeeSearchParams
from app.schemas.employee_schema import EmployeeRead, PaginationResponse
from app.servicelog.servicelog import logger


class EmployeeService:
    def __init__(self, db: Session):
        self.db = db
        self.emp_repo = EmployeeRepository(db)
        self.org_repo = OrganizationRepository(db)
        self.config = config

    def build_dynamic_field_response(self, employee: Employee, org_id: int | None = None) -> dict[str, Any]:
        output_fields = self.config.get_enabled_columns(org_id)
        result = {}

        RELATIONSHIP_MAP = {
            "department": lambda e: e.department.name if e.department else None,
            "position":   lambda e: e.position.name   if e.position   else None,
            "location":   lambda e: e.location.name   if e.location   else None,
            "company":    lambda e: e.company.name    if e.company    else None,
            "status":     lambda e: e.status.name     if e.status     else None,
        }

        for field in output_fields:
            if field in RELATIONSHIP_MAP:
                result[field] = RELATIONSHIP_MAP[field](employee)
            else:
                result[field] = getattr(employee, field, None)

        return result

    def search(self, params: EmployeeSearchParams, x_org_key: str) -> PaginationResponse:
        logger.info("Service start handling request.")
        organization_id = self.org_repo.get_organization_id_by_api_key(x_org_key)
        if not organization_id:
            raise HTTPException(status_code=403, detail="Invalid organization key")

        filters = {
            k: v for k, v in {
                "name": params.name,
                "department_id": params.department_id,
                "position_id": params.position_id,
                "location_id": params.location_id,
                "status_id": params.status_id,
                "company_id": params.company_id,
                "organization_id": organization_id
            }.items() if v is not None
        }

        skip = (params.page - 1) * params.size
        limit = params.size

        logger.info(f"Service send request to repository with filters={filters}, skip={skip}, limit={limit}")
        employees, total = self.emp_repo.search(filters=filters, skip=skip, limit=limit)

        included_fields = set(self.config.get_enabled_columns(organization_id))

        data = []
        for emp in employees:
            emp_data = {
                "id": emp.id,
                "first_name": emp.first_name,
                "last_name": emp.last_name,
                "contact": emp.contact,
                "department": emp.department.name if emp.department else None,
                "location": emp.location.name if emp.location else None,
                "position": emp.position.name if emp.position else None,
                "status": emp.status.name if emp.status else None,
                "company": emp.company.name if emp.company else None,
            }
            # validate by pydantic model
            data.append(EmployeeRead(**emp_data).model_dump(include=included_fields))

        return PaginationResponse(
                    page=params.page,
                    size=params.size,
                    total=total,
                    total_pages=(total + params.size - 1) // params.size,
                    data=data
                )
