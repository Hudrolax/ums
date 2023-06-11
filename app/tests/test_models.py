import psycopg2
import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from core.config import DB_HOST, DB_USER, DB_PASS
from datetime import date, time
from typing import Generator
from api.v1.buildings.model import BuildingDB
from api.v1.semesters.model import SemesterDB
from api.v1.faculties.model import FacultyDB
from api.v1.classrooms.model import ClassroomDB
from api.v1.departments.model import DepartmentDB
from api.v1.teachers.model import TeacherDB
from api.v1.courses.model import CourseDB
from api.v1.course_programs.model import CourseProgramDB
from api.v1.groups.model import GroupDB
from api.v1.study_plans.model import StudyPlanDB
from api.v1.students.model import StudentDB
from api.v1.schedules.model import ScheduleDB
from api.v1.exams.model import ExamDB
from api.v1.grades.model import GradeDB
from api.v1.assignments.model import AssignmentDB

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:5432/postgres"
TEST_DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:5432/test_models_db"


def apply_migrations(database_url: str) -> None:
    """Create tables in the test DB.

    Args:
        database_url (str): Test base URL
    """
    engine = create_engine(database_url)
    with open('db/queries/create_tables.sql') as f:
        with engine.begin() as connection:
            connection.execute(text(f.read()))


@pytest.fixture(scope="session", autouse=True)
def create_db() -> Generator:
    """The function creates and deletes a test data base."""
    conn = psycopg2.connect(DATABASE_URL)
    conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = conn.cursor()

    cursor.execute("DROP DATABASE IF EXISTS test_models_db;")
    cursor.execute("CREATE DATABASE test_models_db;")
    cursor.close()
    conn.close()

    apply_migrations(TEST_DATABASE_URL)

    yield

    conn = psycopg2.connect(DATABASE_URL)
    conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = conn.cursor()
    cursor.execute(f"""
        SELECT 
            pg_terminate_backend(pg_stat_activity.pid)
        FROM 
            pg_stat_activity
        WHERE 
            pg_stat_activity.datname = 'test_models_db'
            AND pid <> pg_backend_pid();
    """)
    cursor.execute("DROP DATABASE IF EXISTS test_models_db;")
    cursor.close()
    conn.close()


@pytest.fixture(scope="session")
def db() -> Generator:
    """The function makes session for tests."""
    engine = create_engine(TEST_DATABASE_URL)
    connection = engine.connect()
    transaction = connection.begin()
    session = sessionmaker(autocommit=False, autoflush=False, bind=engine)()

    try:
        yield session
    finally:
        session.close()
        transaction.rollback()
        connection.close()


def test_create_building(db) -> None:
    """Testing the creation of a Building and adding it to the DB."""
    new_building = BuildingDB(name="Test building", address="123 Test St")

    db.add(new_building)
    db.flush()
    db.refresh(new_building)

    assert new_building.name == "Test building"
    assert new_building.address == "123 Test St"

    db_building = db.query(BuildingDB).filter_by(name="Test building").first()

    assert db_building is not None
    assert db_building.name == "Test building"
    assert db_building.address == "123 Test St"

def test_create_semester(db) -> None:
    """Testing the creation of a Semester and adding it to the DB."""
    new_semester = SemesterDB(year=2020, semester=1)

    db.add(new_semester)
    db.flush()
    db.refresh(new_semester)

    assert new_semester.year == 2020
    assert new_semester.semester == 1

    db_semester = db.query(SemesterDB).filter_by(year=2020, semester=1).first()

    assert db_semester is not None
    assert db_semester.year == 2020
    assert db_semester.semester == 1

def test_create_faculty(db):
    """Testing the creation of a Faculty and adding it to the DB."""
    new_faculty = FacultyDB(name='Mathematic')

    db.add(new_faculty)
    db.flush()
    db.refresh(new_faculty)

    assert new_faculty.name == 'Mathematic'

    db_faculty = db.query(FacultyDB).filter_by(name='Mathematic').first()

    assert db_faculty is not None
    assert db_faculty.name == 'Mathematic'

def test_create_classroom(db) -> None:
    """Testing the creation of a Classroom and adding it to the DB."""
    new_building = BuildingDB(name="Test building", address="123 Test St")
    db.add(new_building)
    db.flush()
    
    new_classroom = ClassroomDB(number=101, capacity=50, buildingId=new_building.id)
    db.add(new_classroom)
    db.flush()

    assert new_classroom.number == 101
    assert new_classroom.capacity == 50
    assert new_classroom.buildingId == new_building.id

    db.refresh(new_classroom)

    db_classroom = db.query(ClassroomDB).filter_by(number=101).first()

    assert db_classroom is not None
    assert db_classroom.number == 101
    assert db_classroom.capacity == 50
    assert db_classroom.buildingId == new_building.id

def test_create_department(db) -> None:
    """Testing the creation of a Faculty and adding it to the DB."""
    new_faculty = FacultyDB(name="Test faculty")
    db.add(new_faculty)
    db.flush()
    
    new_department = DepartmentDB(name="Test department", facultyId=new_faculty.id)
    db.add(new_department)
    db.flush()

    assert new_department.name == "Test department"
    assert new_department.facultyId == new_faculty.id

    db.refresh(new_department)

    db_department = db.query(DepartmentDB).filter_by(name="Test department").first()

    assert db_department is not None
    assert db_department.name == "Test department"
    assert db_department.facultyId == new_faculty.id

def test_create_teacher(db) -> None:
    """Testing the creation of a Teacher and adding it to the DB."""
    new_faculty = FacultyDB(name="Test faculty")
    db.add(new_faculty)
    db.flush()

    new_teacher = TeacherDB(firstName="Test", lastName="Teacher", email="test.teacher@example.com", facultyId=new_faculty.id)
    db.add(new_teacher)
    db.flush()

    assert new_teacher.firstName == "Test"
    assert new_teacher.lastName == "Teacher"
    assert new_teacher.email == "test.teacher@example.com"
    assert new_teacher.facultyId == new_faculty.id

    db.refresh(new_teacher)

    db_teacher = db.query(TeacherDB).filter_by(email="test.teacher@example.com").first()

    assert db_teacher is not None
    assert db_teacher.firstName == "Test"
    assert db_teacher.lastName == "Teacher"
    assert db_teacher.email == "test.teacher@example.com"
    assert db_teacher.facultyId == new_faculty.id

def test_create_course(db) -> None:
    """Testing the creation of a Course and adding it to the DB."""
    new_faculty = FacultyDB(name="Test faculty")
    db.add(new_faculty)
    db.flush()

    new_teacher = TeacherDB(firstName="Test", lastName="Teacher", email="test.teacher@example.com", facultyId=new_faculty.id)
    db.add(new_teacher)
    db.flush()

    new_course = CourseDB(name="Test course", teacherId=new_teacher.id)
    db.add(new_course)
    db.flush()

    assert new_course.name == "Test course"
    assert new_course.teacherId == new_teacher.id

    db.refresh(new_course)

    db_course = db.query(CourseDB).filter_by(name="Test course").first()

    assert db_course is not None
    assert db_course.name == "Test course"
    assert db_course.teacherId == new_teacher.id

def test_create_course_program(db) -> None:
    """Testing the creation of a Course Program and adding it to the DB."""
    new_faculty = FacultyDB(name="Test faculty")
    db.add(new_faculty)
    db.flush()

    new_teacher = TeacherDB(firstName="Test", lastName="Teacher", email="test.teacher@example.com", facultyId=new_faculty.id)
    db.add(new_teacher)
    db.flush()

    new_course = CourseDB(name="Test course", teacherId=new_teacher.id)
    db.add(new_course)
    db.flush()

    new_course_program = CourseProgramDB(description="Test description", courseId=new_course.id)
    db.add(new_course_program)
    db.flush()

    assert new_course_program.description == "Test description"
    assert new_course_program.courseId == new_course.id

    db.refresh(new_course_program)

    db_course_program = db.query(CourseProgramDB).filter_by(description="Test description").first()

    assert db_course_program is not None
    assert db_course_program.description == "Test description"
    assert db_course_program.courseId == new_course.id

def test_create_group(db) -> None:
    """Testing the creation of a Group and adding it to the DB."""
    new_faculty = FacultyDB(name="Test faculty")
    db.add(new_faculty)
    db.flush()

    new_department = DepartmentDB(name="Test department", facultyId=new_faculty.id)
    db.add(new_department)
    db.flush()

    new_teacher = TeacherDB(firstName="Test", lastName="Teacher", email="test.teacher@example.com", facultyId=new_faculty.id)
    db.add(new_teacher)
    db.flush()

    new_course = CourseDB(name="Test course", teacherId=new_teacher.id)
    db.add(new_course)
    db.flush()

    new_group = GroupDB(name="Test group", departmentId=new_department.id, courseId=new_course.id)
    db.add(new_group)
    db.flush()

    assert new_group.name == "Test group"
    assert new_group.departmentId == new_department.id
    assert new_group.courseId == new_course.id

    db.refresh(new_group)

    db_group = db.query(GroupDB).filter_by(name="Test group").first()

    assert db_group is not None
    assert db_group.name == "Test group"
    assert db_group.departmentId == new_department.id
    assert db_group.courseId == new_course.id

def test_create_study_plan(db) -> None:
    """Testing the creation of a study plan and adding it to the DB."""
    new_semester = SemesterDB(year=2023, semester=1)
    db.add(new_semester)
    db.flush()

    new_faculty = FacultyDB(name="Test faculty")
    db.add(new_faculty)
    db.flush()

    new_department = DepartmentDB(name="Test department", facultyId=new_faculty.id)
    db.add(new_department)
    db.flush()

    new_teacher = TeacherDB(firstName="Test", lastName="Teacher", email="test.teacher@example.com", facultyId=new_faculty.id)
    db.add(new_teacher)
    db.flush()

    new_course = CourseDB(name="Test course", teacherId=new_teacher.id)
    db.add(new_course)
    db.flush()

    new_group = GroupDB(name="Test group", departmentId=new_department.id, courseId=new_course.id)
    db.add(new_group)
    db.flush()

    new_study_plan = StudyPlanDB(description="Test study plan", semesterId=new_semester.id, courseId=new_course.id, groupId=new_group.id)
    db.add(new_study_plan)
    db.flush()

    assert new_study_plan.description == "Test study plan"
    assert new_study_plan.semesterId == new_semester.id
    assert new_study_plan.courseId == new_course.id
    assert new_study_plan.groupId == new_group.id

    db.refresh(new_study_plan)

    db_study_plan = db.query(StudyPlanDB).filter_by(description="Test study plan").first()

    assert db_study_plan is not None
    assert db_study_plan.description == "Test study plan"
    assert db_study_plan.semesterId == new_semester.id
    assert db_study_plan.courseId == new_course.id
    assert db_study_plan.groupId == new_group.id

def test_create_student(db) -> None:
    """Testing the creation of a Student and adding it to the DB."""
    new_faculty = FacultyDB(name="Test faculty")
    db.add(new_faculty)
    db.flush()

    new_department = DepartmentDB(name="Test department", facultyId=new_faculty.id)
    db.add(new_department)
    db.flush()

    new_teacher = TeacherDB(firstName="Test", lastName="Teacher", email="test.teacher@example.com", facultyId=new_faculty.id)
    db.add(new_teacher)
    db.flush()

    new_course = CourseDB(name="Test course", teacherId=new_teacher.id)
    db.add(new_course)
    db.flush()

    new_group = GroupDB(name="Test group", departmentId=new_department.id, courseId=new_course.id)
    db.add(new_group)
    db.flush()

    new_student = StudentDB(firstName="Test", lastName="Student", email="test.student@example.com", groupId=new_group.id)
    db.add(new_student)
    db.flush()

    assert new_student.firstName == "Test"
    assert new_student.lastName == "Student"
    assert new_student.email == "test.student@example.com"
    assert new_student.groupId == new_group.id

    db.refresh(new_student)

    db_student = db.query(StudentDB).filter_by(email="test.student@example.com").first()

    assert db_student is not None
    assert db_student.firstName == "Test"
    assert db_student.lastName == "Student"
    assert db_student.email == "test.student@example.com"
    assert db_student.groupId == new_group.id

def test_create_schedule(db) -> None:
    """Testing the creation of a Schedule and adding it to the DB."""
    new_building = BuildingDB(name="Test building", address="123 Test St")
    db.add(new_building)
    db.flush()

    new_classroom = ClassroomDB(number=101, capacity=50, buildingId=new_building.id)
    db.add(new_classroom)
    db.flush()

    new_faculty = FacultyDB(name="Test faculty")
    db.add(new_faculty)
    db.flush()

    new_teacher = TeacherDB(firstName="Test", lastName="Teacher", email="test.teacher@example.com", facultyId=new_faculty.id)
    db.add(new_teacher)
    db.flush()

    new_course = CourseDB(name="Test course", teacherId=new_teacher.id)
    db.add(new_course)
    db.flush()

    new_schedule = ScheduleDB(date=date.today(), time=time(hour=10), courseId=new_course.id, classroomId=new_classroom.id)
    db.add(new_schedule)
    db.flush()

    assert new_schedule.date == date.today()
    assert new_schedule.time == time(hour=10)
    assert new_schedule.courseId == new_course.id
    assert new_schedule.classroomId == new_classroom.id

    db.refresh(new_schedule)

    db_schedule = db.query(ScheduleDB).filter_by(date=date.today(), time=time(hour=10)).first()

    assert db_schedule is not None
    assert db_schedule.date == date.today()
    assert db_schedule.time == time(hour=10)
    assert db_schedule.courseId == new_course.id
    assert db_schedule.classroomId == new_classroom.id

def test_create_exam(db) -> None:
    """Testing the creation of an Exam and adding it to the DB."""
    new_building = BuildingDB(name="Test building", address="123 Test St")
    db.add(new_building)
    db.flush()

    new_classroom = ClassroomDB(number=101, capacity=50, buildingId=new_building.id)
    db.add(new_classroom)
    db.flush()

    new_faculty = FacultyDB(name="Test faculty")
    db.add(new_faculty)
    db.flush()

    new_teacher = TeacherDB(firstName="Test", lastName="Teacher", email="test.teacher@example.com", facultyId=new_faculty.id)
    db.add(new_teacher)
    db.flush()

    new_course = CourseDB(name="Test course", teacherId=new_teacher.id)
    db.add(new_course)
    db.flush()

    new_exam = ExamDB(date=date.today(), time=time(hour=10), courseId=new_course.id, classroomId=new_classroom.id)
    db.add(new_exam)
    db.flush()

    assert new_exam.date == date.today()
    assert new_exam.time == time(hour=10)
    assert new_exam.courseId == new_course.id
    assert new_exam.classroomId == new_classroom.id

    db.refresh(new_exam)

    db_exam = db.query(ExamDB).filter_by(date=date.today(), time=time(hour=10)).first()

    assert db_exam is not None
    assert db_exam.date == date.today()
    assert db_exam.time == time(hour=10)
    assert db_exam.courseId == new_course.id
    assert db_exam.classroomId == new_classroom.id

def test_create_grade(db) -> None:
    """Testing the creation of a Grade and adding it to the DB."""
    new_faculty = FacultyDB(name="Test faculty")
    db.add(new_faculty)
    db.flush()

    new_department = DepartmentDB(name="Test department", facultyId=new_faculty.id)
    db.add(new_department)
    db.flush()

    new_teacher = TeacherDB(firstName="Test", lastName="Teacher", email="test.teacher@example.com", facultyId=new_faculty.id)
    db.add(new_teacher)
    db.flush()

    new_course = CourseDB(name="Test course", teacherId=new_teacher.id)
    db.add(new_course)
    db.flush()

    new_group = GroupDB(name="Test group", departmentId=new_department.id, courseId=new_course.id)
    db.add(new_group)
    db.flush()

    new_student = StudentDB(firstName="Test", lastName="Student", email="test.student@example.com", groupId=new_group.id)
    db.add(new_student)
    db.flush()

    new_grade = GradeDB(grade=95, studentId=new_student.id, courseId=new_course.id)
    db.add(new_grade)
    db.flush()

    assert new_grade.grade == 95
    assert new_grade.studentId == new_student.id
    assert new_grade.courseId == new_course.id

    db.refresh(new_grade)

    db_grade = db.query(GradeDB).filter_by(grade=95, studentId=new_student.id).first()

    assert db_grade is not None
    assert db_grade.grade == 95
    assert db_grade.studentId == new_student.id
    assert db_grade.courseId == new_course.id

def test_create_assignment(db) -> None:
    """Testing the creation of a Assignment and adding it to the DB."""
    new_faculty = FacultyDB(name="Test faculty")
    db.add(new_faculty)
    db.flush()

    new_teacher = TeacherDB(firstName="Test", lastName="Teacher", email="test.teacher@example.com", facultyId=new_faculty.id)
    db.add(new_teacher)
    db.flush()

    new_course = CourseDB(name="Test course", teacherId=new_teacher.id)
    db.add(new_course)
    db.flush()

    new_assignment = AssignmentDB(description="Test assignment", dateAssigned=date.today(), dueDate=date.today(), courseId=new_course.id)
    db.add(new_assignment)
    db.flush()

    assert new_assignment.description == "Test assignment"
    assert new_assignment.dateAssigned == date.today()
    assert new_assignment.dueDate == date.today()
    assert new_assignment.courseId == new_course.id

    db.refresh(new_assignment)

    db_assignment = db.query(AssignmentDB).filter_by(description="Test assignment", courseId=new_course.id).first()

    assert db_assignment is not None
    assert db_assignment.description == "Test assignment"
    assert db_assignment.dateAssigned == date.today()
    assert db_assignment.dueDate == date.today()
    assert db_assignment.courseId == new_course.id
