# University management systems
## DB Structure
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
