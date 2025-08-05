# api/employee_router.py
from fastapi import APIRouter, Depends, Request, Header
from sqlalchemy.orm import Session
from typing import List, Any

from app.schemas.employee_schema import EmployeeRead
from app.services.employee_service import search_employees_service
from app.core.database import get_db
from app.api.employee_param import EmployeeSearchParams
from app.servicelog.servicelog import logger
from app.rate_limiting.fixed_window import FixedWindowLimiter
from app.rate_limiting.rate_limiter import rate_limited
from app.config.config import Config


router = APIRouter()

# 💡 Create limiter instance (per-IP + global limit)
# Limiter's configuration will be read from CONFIG_PATH
limiter = FixedWindowLimiter()

@router.get("/employees/search", response_model=List[dict[str, Any]])
@rate_limited(limiter)
def search_employees(
    request: Request,
    x_org_key: str = Header(..., alias="X-ORG-KEY"),
    params: EmployeeSearchParams = Depends(),
    db: Session = Depends(get_db)
)-> List[dict[str, Any]]:
    # TODO: Exception handle
    logger.info(f"Receive request: param={params}")
    return search_employees_service(params, db, x_org_key)
