from pydantic import BaseModel, ConfigDict

class EmployeeRead(BaseModel):
    id: int
    first_name: str
    last_name: str
    contact: str
    department: str
    location: str
    position: str
    status: str
    company: str

    model_config = ConfigDict(from_attributes=True)
