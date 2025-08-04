# api/employee_router.py
from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from typing import List, Any

from app.schemas.employee_schema import EmployeeRead
from app.services.employee_service import search_employees_service
from app.core.database import get_db
from app.api.employee_param import EmployeeSearchParams
from app.servicelog.servicelog import logger
from app.rate_limiting.fixed_window import FixedWindowLimiter
from app.rate_limiting.rate_limiter import rate_limited

router = APIRouter()

# 💡 Create limiter instance (per-IP + global limit)
limiter = FixedWindowLimiter(
    max_requests=10,           # per-IP limit
    window_seconds=60,         # window time
    max_global_requests=1000   # optional global limit across all clients
)

@router.get("/employees/search", response_model=List[dict[str, Any]])
@rate_limited(limiter)
def search_employees(
    request: Request,
    params: EmployeeSearchParams = Depends(),
    db: Session = Depends(get_db)
)-> List[dict[str, Any]]:
    # TODO: Exception handle
    logger.info(f"Receive request: param={params}")
    return search_employees_service(params, db)
