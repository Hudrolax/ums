SELECT 
    "Students"."firstName",
    "Students"."lastName"
FROM
    "Students"
JOIN 
    "Groups" ON "Students"."groupId" = "Groups".id
JOIN 
    "Departments" ON "Groups"."departmentId" = "Departments".id
WHERE 
    "Departments"."facultyId" = (SELECT id FROM "Faculties" WHERE name = 'Математика');
