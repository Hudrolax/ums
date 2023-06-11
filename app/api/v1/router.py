from fastapi import APIRouter
from .teachers.router import router as teachers_router
from .students.router import router as students_router
from .courses.router import router as courses_router
from .grades.router import router as grades_router

router = APIRouter()

router.include_router(teachers_router, prefix='/teachers', tags=['Teachers'])
router.include_router(students_router, prefix='/students', tags=['Students'])
router.include_router(courses_router, prefix='/courses', tags=['Courses'])
router.include_router(grades_router, prefix='/grades', tags=['Grades'])
