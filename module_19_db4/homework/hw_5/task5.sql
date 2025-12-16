SELECT sg.group_id,
       COUNT(DISTINCT s.student_id) AS total_students,
       AVG(g.grade) AS avg_grade,
       SUM(CASE WHEN g.grade IS NULL THEN 1 ELSE 0 END) AS not_submitted,
       SUM(CASE WHEN g.date > a.due_date THEN 1 ELSE 0 END) AS overdue,
       SUM(CASE WHEN g.grade_id IS NOT NULL
                 AND (SELECT COUNT(*)
                      FROM assignments_grades g2
                      WHERE g2.student_id = s.student_id
                        AND g2.assisgnment_id = g.assisgnment_id) > 1
                THEN 1 ELSE 0 END) AS retries
FROM students s
JOIN assignments_grades g ON s.student_id = g.student_id
JOIN assignments a ON g.assisgnment_id = a.assisgnment_id
JOIN students_groups sg ON a.group_id = sg.group_id
GROUP BY sg.group_id
ORDER BY sg.group_id;
