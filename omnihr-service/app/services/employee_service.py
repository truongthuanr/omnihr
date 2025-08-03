# services/employee_service.py
from sqlalchemy.orm import Session

from app.api.employee_param import EmployeeSearchParams
from app.repositories.employee_repository import EmployeeRepository
from app.servicelog.servicelog import logger


def search_employees_service(params: EmployeeSearchParams, db: Session):
    
    logger.info(f"Service start handling request.")
    repository = EmployeeRepository(db)
    filters = {
        "department_id": params.department_id,
        "position_id": params.position_id,
        "location_id": params.location_id,
        "status_id": params.status_id,
        "company_id": params.company_id
    }
    _skip = (params.page - 1) * params.size
    _limit = params.size
    logger.info(f"Service send request to repository with filter={filters}, skip={_skip}, limit={_limit}")
    return repository.search(
        filters=filters,
        skip=_skip,
        limit=_limit
    )
