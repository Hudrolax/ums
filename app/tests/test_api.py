import psycopg2
import pytest
from typing import Generator
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session
from core.config import DB_HOST, DB_USER, DB_PASS
from main import app
from core.database import get_db
from api.v1.teachers.model import TeacherDB
from api.v1.students.model import StudentDB
from api.v1.grades.model import GradeDB
from api.v1.courses.model import CourseDB
from api.v1.groups.model import GroupDB


DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:5432/postgres"
TEST_DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:5432/test_api_db"

engine = create_engine(TEST_DATABASE_URL)
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_test_db() -> Generator:
    try:
        db = TestSessionLocal()
        yield db
    finally:
        db.close()


# override the get_db function for the app
app.dependency_overrides[get_db] = get_test_db
client = TestClient(app)


def apply_migrations(database_url: str) -> None:
    """Create tables in the test DB.

    Args:
        database_url (str): Test base URL
    """
    engine = create_engine(database_url)
    with open('db/queries/create_tables.sql') as f:
        with engine.begin() as connection:
            connection.execute(text(f.read()))
    with open('db/queries/fill_db.sql') as f:
        with engine.begin() as connection:
            connection.execute(text(f.read()))


@pytest.fixture(scope="session", autouse=True)
def create_db() -> Generator:
    """The function creates and deletes a test data base."""
    conn = psycopg2.connect(DATABASE_URL)
    conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = conn.cursor()

    cursor.execute("DROP DATABASE IF EXISTS test_api_db;")
    cursor.execute("CREATE DATABASE test_api_db;")
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
            pg_stat_activity.datname = 'test_api_db'
            AND pid <> pg_backend_pid();
    """)
    cursor.execute("DROP DATABASE IF EXISTS test_api_db;")
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


@pytest.fixture
def new_student():
    return {
        "firstName": "Test",
        "lastName": "Student",
        "email": "test.student@example.com",
        "groupId": 1
    }


@pytest.fixture
def new_course():
    return {
        "name": "New test course",
        "teacherId": 1
    }


def test_get_teachers(db: Session):
    new_teacher = TeacherDB(firstName="Test", lastName="Teacher",
                            email="test.teacher@example.com", facultyId=1)
    db.add(new_teacher)
    db.commit()
    db.refresh(new_teacher)

    response = client.get("api/v1/teachers/")

    assert response.status_code == 200
    teachers = response.json()

    assert len(teachers) > 0
    assert teachers[-1]['firstName'] == "Test"
    assert teachers[-1]['lastName'] == "Teacher"
    assert teachers[-1]['email'] == "test.teacher@example.com"

    db_teacher = db.query(TeacherDB).filter_by(
        email="test.teacher@example.com").first()

    assert db_teacher is not None
    assert db_teacher.firstName == "Test"
    assert db_teacher.lastName == "Teacher"
    assert db_teacher.email == "test.teacher@example.com"
    assert db_teacher.facultyId == 1

    db.delete(db_teacher)
    db.commit()


def test_get_student_by_id(db) -> None:
    """Test get a student by the id."""
    existing_student = StudentDB(firstName="Test", lastName="Student",
                                 email="test.student@example.com", groupId=1)
    db.add(existing_student)
    db.commit()
    db.refresh(existing_student)

    response = client.get(f"api/v1/students/{existing_student.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["firstName"] == "Test"
    assert data["lastName"] == "Student"
    assert data["email"] == "test.student@example.com"
    assert data["groupId"] == 1
    assert "id" in data
    assert data["id"] == existing_student.id

    db.delete(existing_student)
    db.commit()


def test_create_student(db, new_student) -> None:
    """Test creating a new student."""
    response = client.post("api/v1/students/", json=new_student)
    assert response.status_code == 200
    data = response.json()
    assert data["firstName"] == "Test"
    assert data["lastName"] == "Student"
    assert data["email"] == "test.student@example.com"
    assert data["groupId"] == 1
    assert "id" in data
    student_id = data["id"]

    db_student = db.query(StudentDB).filter_by(id=student_id).first()
    assert db_student is not None
    assert db_student.firstName == "Test"
    assert db_student.lastName == "Student"
    assert db_student.email == "test.student@example.com"
    assert db_student.groupId == 1

    db.delete(db_student)
    db.commit()


def test_create_student_with_existing_email(db, new_student) -> None:
    """Test creating a new student with an existing email."""
    existing_student = StudentDB(firstName="Test", lastName="Student",
                                 email="test.student@example.com", groupId=1)
    db.add(existing_student)
    db.commit()
    db.refresh(existing_student)

    response = client.post("api/v1/students/", json=new_student)
    assert response.status_code == 409

    db_student = db.query(StudentDB).filter_by(
        email='test.student@example.com').all()
    assert db_student is not None
    assert len(db_student) == 1

    db.delete(db_student[0])
    db.commit()


def test_update_student(db, new_student) -> None:
    """Test update a student."""
    existing_student = StudentDB(firstName="Test", lastName="Student",
                                 email="test.student@example.com", groupId=1)
    db.add(existing_student)
    db.commit()

    new_student['email'] = 'newemail@example.com'

    response = client.put(
        f"api/v1/students/{existing_student.id}", json=new_student)
    assert response.status_code == 200

    db.refresh(existing_student)
    db_student = db.query(StudentDB).filter_by(id=existing_student.id).first()
    assert db_student is not None
    assert db_student.email == 'newemail@example.com'

    # test update with exist email
    exist_student2 = StudentDB(firstName="Test2", lastName="Student2",
                               email="test.student2@example.com", groupId=1)
    db.add(exist_student2)
    db.commit()

    new_student['email'] = 'test.student2@example.com'
    response = client.put(
        f"api/v1/students/{existing_student.id}", json=new_student)
    assert response.status_code == 409

    # test update not available student
    response = client.put("api/v1/students/99", json=new_student)
    assert response.status_code == 404

    db.delete(db_student)
    db.delete(exist_student2)
    db.commit()


def test_delete_student(db) -> None:
    """Test delete an exists student."""
    existing_student = StudentDB(firstName="Test", lastName="Student",
                                 email="test.student@example.com", groupId=1)
    db.add(existing_student)
    db.commit()

    # test deleting existing student
    response = client.delete(
        f"api/v1/students/{existing_student.id}")
    assert response.status_code == 200

    db_student = db.query(StudentDB).filter_by(id=existing_student.id).first()
    assert db_student is None

    # test delete not available student
    response = client.delete(
        f"api/v1/students/999999")
    assert response.status_code == 404

    # test cascade delete grades with exists student from migrations with id == 1
    db_grades = db.query(GradeDB).filter_by(studentId=1).first()
    assert db_grades is not None

    response = client.delete(f"api/v1/students/1")
    assert response.status_code == 200

    db_grades = db.query(GradeDB).filter_by(studentId=1).first()
    assert db_grades is None


def test_get_course_by_id(db) -> None:
    """Test get a course by the id."""
    existing_course = CourseDB(name="Test course", teacherId=1)
    db.add(existing_course)
    db.commit()
    db.refresh(existing_course)

    response = client.get(f"api/v1/courses/{existing_course.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test course"
    assert data["teacherId"] == 1
    assert "id" in data
    assert data["id"] == existing_course.id

    db.delete(existing_course)
    db.commit()


def test_create_course(db, new_course) -> None:
    """Test creating a new course."""
    response = client.post("api/v1/courses/", json=new_course)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "New test course"
    assert data["teacherId"] == 1
    assert "id" in data
    course_id = data["id"]

    db_course = db.query(CourseDB).filter_by(id=course_id).first()
    assert db_course is not None
    assert db_course.name == "New test course"
    assert db_course.teacherId == 1

    response = client.post("api/v1/courses/", json=new_course)
    assert response.status_code == 409

    new_course['teacherId'] = 99999
    response = client.post("api/v1/courses/", json=new_course)
    assert response.status_code == 400

    db.delete(db_course)
    db.commit()


def test_get_students_on_course(db) -> None:
    """Test get all students on a course."""

    existing_course = CourseDB(name="Test course", teacherId=1)
    db.add(existing_course)
    db.commit()
    db.refresh(existing_course)

    group = GroupDB(name="Test Group", departmentId=1,
                    courseId=existing_course.id)
    db.add(group)
    db.commit()
    db.refresh(group)

    student1 = StudentDB(firstName="Test1", lastName="Student1",
                         email="test1.student@example.com", groupId=group.id)
    student2 = StudentDB(firstName="Test2", lastName="Student2",
                         email="test2.student@example.com", groupId=group.id)
    db.add(student1)
    db.add(student2)

    db.commit()
    db.refresh(student1)
    db.refresh(student2)

    response = client.get(f"api/v1/courses/{existing_course.id}/students")
    assert response.status_code == 200
    data = response.json()

    assert len(data) == 2

    students_data = {student["id"]: student for student in data}
    assert students_data[student1.id]["firstName"] == "Test1"
    assert students_data[student1.id]["lastName"] == "Student1"
    assert students_data[student1.id]["email"] == "test1.student@example.com"
    assert students_data[student2.id]["firstName"] == "Test2"
    assert students_data[student2.id]["lastName"] == "Student2"
    assert students_data[student2.id]["email"] == "test2.student@example.com"

    db.delete(student1)
    db.delete(student2)
    db.delete(group)
    db.delete(existing_course)
    db.commit()


def test_create_grade(db) -> None:
    """Test creating a new grade."""
    course = CourseDB(name="Test course", teacherId=1)
    db.add(course)
    db.commit()
    db.refresh(course)

    group = GroupDB(name="Test Group", departmentId=1,
                    courseId=course.id)
    db.add(group)
    db.commit()
    db.refresh(group)

    student = StudentDB(firstName="Test1", lastName="Student1",
                         email="test1.student@example.com", groupId=group.id)
    db.add(student)

    db.commit()
    db.refresh(student)


    new_grade = dict(grade=5, studentId=student.id, courseId=course.id)
    response = client.post("api/v1/grades/", json=new_grade)
    assert response.status_code == 200
    data = response.json()
    assert data["grade"] == 5
    assert data["studentId"] == student.id
    assert data["courseId"] == course.id
    assert "id" in data
    grade_id = data["id"]

    db_grade = db.query(GradeDB).filter_by(id=grade_id).first()
    assert db_grade is not None
    assert db_grade.grade == 5
    assert db_grade.studentId == student.id
    assert db_grade.courseId == course.id

    response = client.post("api/v1/grades/", json=new_grade)
    assert response.status_code == 409

    grade_wrong_student = new_grade.copy()
    grade_wrong_student['studentId'] = 9999
    response = client.post("api/v1/grades/", json=grade_wrong_student)
    assert response.status_code == 400

    grade_wrong_course = new_grade.copy()
    grade_wrong_course['courseId'] = 9999
    response = client.post("api/v1/grades/", json=grade_wrong_course)
    assert response.status_code == 400

    db.delete(course)
    db.delete(group)
    db.delete(student)
    db.delete(db_grade)
    db.commit()


def test_update_grade(db) -> None:
    """Test update a grade."""
    existing_grade = db.query(GradeDB).filter_by(studentId=2, courseId=2).first()

    new_grade = dict(grade=21, studentId=2, courseId=2)

    response = client.put(
        f"api/v1/grades/{existing_grade.id}", json=new_grade)
    assert response.status_code == 200

    db.refresh(existing_grade)
    db_grade = db.query(GradeDB).filter_by(id=existing_grade.id).first()
    assert db_grade is not None
    assert db_grade.grade == 21
    assert db_grade.studentId == 2
    assert db_grade.courseId == 2

    # test update not available grade
    response = client.put("api/v1/grades/9999", json=new_grade)
    assert response.status_code == 404