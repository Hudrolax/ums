# University management systems
The project implements API for the university management system. The project includes the development of a database structure, writing SQL queries and implementing the following FastAPI endpoints:
```
POST /students - Create a new student.
GET /students/{student_id} - Retrieve information about a student by their ID.
PUT /students/{student_id} - Update information about a student by their ID.
DELETE /students/{student_id} - Delete a student by their ID.
GET /teachers - Retrieve a list of all teachers.
POST /courses - Create a new course.
GET /courses/{course_id} - Retrieve information about a course by its ID.
GET /courses/{course_id}/students - Retrieve a list of all students in a course.
POST /grades - Create a new grade for a student in a course.
PUT /grades/{grade_id} - Update a student's grade in a course.
```
The project also implements unit-tests for data models and API endpoints.

## DB Structure
```
Студент: id (PK), имя, фамилия, email, id_группы (FK)
Преподаватель: id (PK), имя, фамилия, email, id_факультета (FK)
Курс: id (PK), название, id_преподавателя (FK)
Группа: id (PK), название, id_отделения (FK), id_курса (FK)
Отделение: id (PK), название, id_факультета (FK)
Оценка: id (PK), оценка, id_студента (FK), id_курса (FK)
Расписание: id (PK), дата, время, id_курса (FK), id_аудитории (FK)
Здание: id (PK), название, адрес
Аудитория: id (PK), номер, вместимость, id_здания (FK)
Семестр: id (PK), год, семестр
Факультет: id (PK), название
Экзамен: id (PK), дата, время, id_курса (FK), id_аудитории (FK)
Задание для самостоятельной работы: id (PK), описание, дата_выдачи, дата_сдачи, id_курса (FK)
Программа курса: id (PK), описание, id_курса (FK)
Учебный план: id (PK), описание, id_семестра (FK), id_курса (FK), id_группы (FK)
```

## Queries
Создание таблиц: https://github.com/Hudrolax/ums/blob/main/app/db/queries/create_tables.sql

Заполнение таблиц демонстрационными данными: https://github.com/Hudrolax/ums/blob/main/app/db/queries/fill_db.sql

Удаление таблиц: https://github.com/Hudrolax/ums/blob/main/app/db/queries/drop_all_tables.sql

Выбрать всех студентов, обучающихся на курсе "Математика": https://github.com/Hudrolax/ums/blob/main/app/db/queries/query1.sql

Обновить оценку студента по курсу: https://github.com/Hudrolax/ums/blob/main/app/db/queries/query2.sql

Выбрать всех преподавателей, которые преподают в здании №3: https://github.com/Hudrolax/ums/blob/main/app/db/queries/query3.sql

Удалить задание для самостоятельной работы, которое было создано более года назад: https://github.com/Hudrolax/ums/blob/main/app/db/queries/query4.sql

Добавить новый семестр в учебный год: https://github.com/Hudrolax/ums/blob/main/app/db/queries/query5.sql

## FastAPI application
### Dependencies:
1. Docker
2. Docker Compose

### Install:
1. Clone the repository:
```https://github.com/Hudrolax/ums.git```
2. Open the project folder: ```cd ums```
3. Make .env file and fill it. You might copy .env-exapmle ```cp .env-example .env```
For testing, you have to set environ variable DEV=true.
4. Build the project: ```docker-compose build```

### Testing:
Run: ```docker-compose run --rm app sh -c "python wait_for_db.py && pytest"```

### Run the App:
Run: ```docker-compose up```
By default, the application applies two migrations: create tables, and fill tables by demonstration data.

### Using:
The base API endpoint is: http://localhost:8000/api/v1/
The API documentation: http://localhost:8000/docs
The GUI for PostgeSQL: http://localhost:8080/
