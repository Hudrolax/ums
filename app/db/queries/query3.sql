SELECT DISTINCT "Teachers".id, "Teachers"."firstName", "Teachers"."lastName"
FROM "Teachers"
JOIN "Courses" ON "Teachers".id = "Courses"."teacherId"
JOIN "Schedules" ON "Courses".id = "Schedules"."courseId"
JOIN "Classrooms" ON "Schedules"."classroomId" = "Classrooms".id
WHERE "Classrooms"."buildingId" = 3;
