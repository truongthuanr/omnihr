from fastapi import FastAPI
from app.api.employee_router import router as api_router  

description="""
OMNI-HR is a modern, scalable HR platform designed to help organizations manage their workforce efficiently.
"""


app = FastAPI(
    title="OMNI-HR Platform",
    description=description,
    version="1.0.0",
)

app.include_router(api_router)
