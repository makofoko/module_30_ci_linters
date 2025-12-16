SELECT sg.group_id,
       AVG(cnt) AS avg_overdue,
       MAX(cnt) AS max_overdue,
       MIN(cnt) AS min_overdue
FROM (
    SELECT s.student_id, sg.group_id, COUNT(*) AS cnt
    FROM students s
    JOIN assignments_grades g ON s.student_id = g.student_id
    JOIN assignments a ON g.assisgnment_id = a.assisgnment_id
    JOIN students_groups sg ON a.group_id = sg.group_id
    WHERE g.date > a.due_date
    GROUP BY s.student_id, sg.group_id
) AS sub
JOIN students_groups sg ON sub.group_id = sg.group_id
GROUP BY sg.group_id;