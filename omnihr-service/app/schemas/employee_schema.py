from pydantic import BaseModel, ConfigDict
from typing import Optional

class DepartmentRead(BaseModel):
    id: int
    name: str
    model_config = ConfigDict(from_attributes=True)

class LocationRead(BaseModel):
    id: int
    name: str
    model_config = ConfigDict(from_attributes=True)

class PositionRead(BaseModel):
    id: int
    name: str
    model_config = ConfigDict(from_attributes=True)

class StatusRead(BaseModel):
    id: int
    name: str
    model_config = ConfigDict(from_attributes=True)

class CompanyRead(BaseModel):
    id: int
    name: str
    model_config = ConfigDict(from_attributes=True)

class EmployeeRead(BaseModel):
    id: int
    first_name: str
    last_name: str
    contact: Optional[str]
    department: Optional[str]
    location: Optional[str]
    position: Optional[str]
    status: Optional[str]
    company: Optional[str]
    
    model_config = ConfigDict(from_attributes=True)
