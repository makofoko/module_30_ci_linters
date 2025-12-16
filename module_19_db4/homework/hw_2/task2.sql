SELECT s.full_name, AVG(g.grade) AS avg_grade
FROM students s
JOIN assignments_grades g ON s.student_id = g.student_id
GROUP BY s.full_name
ORDER BY avg_grade DESC
LIMIT 10;