SELECT t.full_name, AVG(g.grade) AS avg_grade
FROM teachers t
JOIN assignments a ON t.teacher_id = a.teacher_id
JOIN assignments_grades g ON a.assisgnment_id
GROUP BY t.full_name
ORDER BY avg_grade ASC;