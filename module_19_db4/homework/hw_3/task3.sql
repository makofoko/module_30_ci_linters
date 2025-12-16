SELECT DISTINCT s.full_name
FROM students s
JOIN assignments_grades g ON s.student_id = g.student_id
JOIN assignments a ON g.assisgnment_id = a.assisgnment_id
WHERE a.teacher_id = (
    SELECT t.teacher_id
    FROM teachers t
    JOIN assignments a ON t.teacher_id = a.teacher_id
    JOIN assignments_grades g ON a.assisgnment_id = g.assisgnment_id
    GROUP BY t.teacher_id
    ORDER BY AVG(g.grade) DESC
    LIMIT 1
);
