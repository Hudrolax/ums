-- Здания. Поля Имя и Адрес
CREATE TABLE "Buildings" (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    address VARCHAR(255)
);
-- Семестры. Поля Год семетра и номер семестра
CREATE TABLE "Semesters" (
    id SERIAL PRIMARY KEY,
    year INT,
    semester INT
);
-- Факультеты. Поля Наименование факультета.
CREATE TABLE "Faculties" (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100)
);
-- Аудитории. Поля Номер аудитории, вместимость, ID здания
CREATE TABLE "Classrooms" (
    id SERIAL PRIMARY KEY,
    number INT,
    capacity INT,
    "buildingId" INT,
    FOREIGN KEY ("buildingId") REFERENCES "Buildings"(id)
);
-- Отделения. Поля Наименование, ID факультета
CREATE TABLE "Departments" (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    "facultyId" INT,
    FOREIGN KEY ("facultyId") REFERENCES "Faculties"(id)
);
-- Преподователи. Поля Имя, Фамилия, e-mail, ID-факультета
CREATE TABLE "Teachers" (
    id SERIAL PRIMARY KEY,
    "firstName" VARCHAR(100),
    "lastName" VARCHAR(100),
    email VARCHAR(100),
    "facultyId" INT,
    FOREIGN KEY ("facultyId") REFERENCES "Faculties"(id)
);
-- Курсы Наименование, ID-преподавателя
CREATE TABLE "Courses" (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    "teacherId" INT,
    FOREIGN KEY ("teacherId") REFERENCES "Teachers"(id)
);
-- Программа курса. Поля Описание, ID-курса
CREATE TABLE "CoursePrograms" (
    id SERIAL PRIMARY KEY,
    description TEXT,
    "courseId" INT,
    FOREIGN KEY ("courseId") REFERENCES "Courses"(id)
);
-- Группы. Поля Имя, id-отделения, id-курса
CREATE TABLE "Groups" (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    "departmentId" INT,
    "courseId" INT,
    FOREIGN KEY ("departmentId") REFERENCES "Departments"(id),
    FOREIGN KEY ("courseId") REFERENCES "Courses"(id)
);
-- Учебный план. Поля Описание плана, id-семестра, id-курса, id-группы
CREATE TABLE "StudyPlans" (
    id SERIAL PRIMARY KEY,
    description TEXT,
    "semesterId" INT,
    "courseId" INT,
    "groupId" INT,
    FOREIGN KEY ("semesterId") REFERENCES "Semesters"(id),
    FOREIGN KEY ("courseId") REFERENCES "Courses"(id),
    FOREIGN KEY ("groupId") REFERENCES "Groups"(id)
);
-- Студенты. Поля Имя, Фамилия, e-mail, id-группы
CREATE TABLE "Students" (
    id SERIAL PRIMARY KEY,
    "firstName" VARCHAR(100),
    "lastName" VARCHAR(100),
    email VARCHAR(100),
    "groupId" INT,
    FOREIGN KEY ("groupId") REFERENCES "Groups"(id)
);
-- Расписания. Поля Дата, время, id-курса, id-аудитории
CREATE TABLE "Schedules" (
    id SERIAL PRIMARY KEY,
    date DATE,
    time TIME,
    "courseId" INT,
    "classroomId" INT,
    FOREIGN KEY ("courseId") REFERENCES "Courses"(id),
    FOREIGN KEY ("classroomId") REFERENCES "Classrooms"(id)
);
-- Экзамены. Поля Дата, Время, id-курса, id-аудитории
CREATE TABLE "Exams" (
    id SERIAL PRIMARY KEY,
    date DATE,
    time TIME,
    "courseId" INT,
    "classroomId" INT,
    FOREIGN KEY ("courseId") REFERENCES "Courses"(id),
    FOREIGN KEY ("classroomId") REFERENCES "Classrooms"(id)
);
-- Оценки. Поля Оценка, id-студента, id-курса
CREATE TABLE "Grades" (
    id SERIAL PRIMARY KEY,
    grade INT,
    "studentId" INT,
    "courseId" INT,
    FOREIGN KEY ("studentId") REFERENCES "Students"(id),
    FOREIGN KEY ("courseId") REFERENCES "Courses"(id)
);
-- Задания для самостоятельной работы. Поля Описание, Дата выдачи, Дата сдачи, id-курса
CREATE TABLE "Assignments" (
    id SERIAL PRIMARY KEY,
    description TEXT,
    "dateAssigned" DATE,
    "dueDate" DATE,
    "courseId" INT,
    FOREIGN KEY ("courseId") REFERENCES "Courses"(id)
);
