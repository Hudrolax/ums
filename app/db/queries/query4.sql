DELETE FROM "Assignments"
WHERE "dateAssigned" < CURRENT_DATE - INTERVAL '1 year';