from fastapi import FastAPI
from api.v1.router import router as api_router
from api.v1.groups.model import GroupDB
from api.v1.students.model import StudentDB
from api.v1.grades.model import GradeDB

app = FastAPI()

app.include_router(api_router, prefix='/api/v1')
