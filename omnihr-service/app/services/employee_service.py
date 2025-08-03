from sqlalchemy.orm import Session
from api.employee_router import EmployeeSearchParams
from repositories.employee_repository import EmployeeRepository


def search_employees_service(params: EmployeeSearchParams, db: Session):
    repository = EmployeeRepository(db)

    filters = {
        "department_id": params.department_id,
        "position_id": params.position_id,
        "location_id": params.location_id,
        "status_id": params.status_id,
        "company_id": params.company_id
    }

    # company_id không bắt buộc → truyền riêng
    return repository.search(
        company_id=params.company_id,
        filters=filters,
        skip=(params.page - 1) * params.size,
        limit=params.size
    )
