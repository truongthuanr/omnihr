# services/employee_service.py
from sqlalchemy.orm import Session
from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.api.employee_param import EmployeeSearchParams
from app.repositories.employee_repository import EmployeeRepository
from app.repositories.origanization_repository import OrganizationRepository
from app.servicelog.servicelog import logger
from app.config.config import config
from app.models.model import Employee

def build_dynamic_field_response(employee: Employee) -> dict:
    output_fields = config.get_enabled_columns()
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

def search_employees_service(params: EmployeeSearchParams, db: Session, x_org_key: str):
    
    logger.info(f"Service start handling request.")
    emp_repo = EmployeeRepository(db)
    org_repo = OrganizationRepository(db)

    organization_id = org_repo.get_organization_id_by_api_key(x_org_key)
    if not organization_id:
        raise HTTPException(status_code=403, detail="Invalid organization key")

    filters = {k: v for k, v in {
        "name": params.name,
        "department_id": params.department_id,
        "position_id": params.position_id,
        "location_id": params.location_id,
        "status_id": params.status_id,
        "company_id": params.company_id,
        "organization_id": organization_id
    }.items() if v is not None}

    _skip = (params.page - 1) * params.size
    _limit = params.size
    logger.info(f"Service send request to repository with filter={filters}, skip={_skip}, limit={_limit}")

    employees =  emp_repo.search(
        filters=filters,
        skip=_skip,
        limit=_limit
    )
    list_emp_response = [build_dynamic_field_response(emp) for emp in employees]
    return list_emp_response
