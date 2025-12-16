SELECT AVG(g.grade) AS avg_grade
FROM assignments_grades g
WHERE g.assisgnment_id IN (
    SELECT a.assisgnment_id
    FROM assignments a
    WHERE a.assignment_text LIKE '%прочит%'
       OR a.assignment_text LIKE '%выуч%'
);