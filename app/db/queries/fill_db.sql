INSERT INTO "Buildings"(name, address) VALUES
('Здание 1', 'адрес 1'),
('Здание 2', 'адрес 2'),
('Здание 3', 'адрес 3');

INSERT INTO "Semesters"(year, semester) VALUES
(2021, 1),
(2021, 2),
(2022, 1),
(2022, 2),
(2023, 1),
(2023, 2);

INSERT INTO "Faculties"(name) VALUES
('Математика'),
('Физика');

INSERT INTO "Classrooms"(number, capacity, "buildingId") VALUES
(101, 50, 1),
(202, 40, 2),
(303, 50, 3);

INSERT INTO "Departments"(name, "facultyId") VALUES
('Отделение 1', 1),
('Отделение 2', 2);

INSERT INTO "Teachers"("firstName", "lastName", email, "facultyId") VALUES
('Вася', 'Пупкин', 'vasyapupkin@example.com', 1),
('Федя', 'Сумкин', 'fedyabaggins@example.com', 2),
('Саша', 'Белый', 'alexwhite@example.com', 2);

INSERT INTO "Courses"(name, "teacherId") VALUES
('Курс 1', 1),
('Курс 2', 2),
('Курс 3', 3);

INSERT INTO "CoursePrograms"(description, "courseId") VALUES
('Описание курса 1', 1),
('Описание курса 2', 2),
('Описание курса 3', 3);

INSERT INTO "Groups"(name, "departmentId", "courseId") VALUES
('Группа 1', 1, 1),
('Группа 2', 2, 2),
('Группа 3', 1, 3);

INSERT INTO "StudyPlans"(description, "semesterId", "courseId", "groupId") VALUES
('План обучения для группы 1', 1, 1, 1),
('План обучения для группы 2', 2, 2, 2),
('План обучения для группы 3', 1, 3, 3);

INSERT INTO "Students"("firstName", "lastName", email, "groupId") VALUES
('Студент1', 'Студентович 1', 'student1@example.com', 1),
('Студент2', 'Студентович 2', 'student2@example.com', 2);

INSERT INTO "Schedules"(date, time, "courseId", "classroomId") VALUES
('2023-01-01', '08:00:00', 1, 1),
('2023-01-01', '08:00:00', 2, 2),
('2023-01-02', '09:00:00', 3, 3);

INSERT INTO "Exams"(date, time, "courseId", "classroomId") VALUES
('2023-06-01', '10:00:00', 1, 1),
('2023-06-02', '11:00:00', 2, 2);

INSERT INTO "Grades"(grade, "studentId", "courseId") VALUES
(90, 1, 1),
(85, 2, 2);

INSERT INTO "Assignments"(description, "dateAssigned", "dueDate", "courseId") VALUES
('Задание 1', '2023-01-01', '2023-01-10', 1),
('Задание 2', '2023-02-01', '2023-02-10', 2),
('Задание 3', '2021-02-01', '2021-02-10', 2);
