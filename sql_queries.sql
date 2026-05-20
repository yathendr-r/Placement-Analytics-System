USE placement_db;
SELECT Placement_Status, COUNT(*) AS Total_Students
FROM placements
GROUP BY Placement_Status;
SELECT ROUND(
    SUM(CASE WHEN Placement_Status = 'Placed' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2
) AS Placement_Percentage
FROM placements;
SELECT Placement_Status, ROUND(AVG(Cgpa), 2) AS Avg_CGPA
FROM placements
GROUP BY Placement_Status;
SELECT Gender, Placement_Status, COUNT(*) AS Count
FROM placements
GROUP BY Gender, Placement_Status
ORDER BY Gender;
SELECT Stream,
    COUNT(*) AS Total,
    SUM(CASE WHEN Placement_Status='Placed' THEN 1 ELSE 0 END) AS Placed,
    ROUND(SUM(CASE WHEN Placement_Status='Placed' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 1) AS Placement_Pct
FROM placements
GROUP BY Stream
ORDER BY Placement_Pct DESC;
SELECT Backlog,
    COUNT(*) AS Total,
    SUM(CASE WHEN Placement_Status='Placed' THEN 1 ELSE 0 END) AS Placed,
    ROUND(SUM(CASE WHEN Placement_Status='Placed' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 1) AS Placement_Pct
FROM placements
GROUP BY Backlog;
SELECT Innovative_Project,
    COUNT(*) AS Total,
    SUM(CASE WHEN Placement_Status='Placed' THEN 1 ELSE 0 END) AS Placed,
    ROUND(SUM(CASE WHEN Placement_Status='Placed' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 1) AS Placement_Pct
FROM placements
GROUP BY Innovative_Project;
SELECT Technical_Course,
    COUNT(*) AS Total,
    SUM(CASE WHEN Placement_Status='Placed' THEN 1 ELSE 0 END) AS Placed,
    ROUND(SUM(CASE WHEN Placement_Status='Placed' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 1) AS Placement_Pct
FROM placements
GROUP BY Technical_Course;
SELECT 
    CASE 
        WHEN Cgpa >= 9.0 THEN '9.0-10.0'
        WHEN Cgpa >= 8.0 THEN '8.0-8.9'
        WHEN Cgpa >= 7.0 THEN '7.0-7.9'
        WHEN Cgpa >= 6.0 THEN '6.0-6.9'
        ELSE 'Below 6.0'
    END AS CGPA_Range,
    COUNT(*) AS Total,
    SUM(CASE WHEN Placement_Status='Placed' THEN 1 ELSE 0 END) AS Placed,
    ROUND(SUM(CASE WHEN Placement_Status='Placed' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 1) AS Placement_Pct
FROM placements
GROUP BY CGPA_Range
ORDER BY Placement_Pct DESC;
SELECT Communication_Score,
    COUNT(*) AS Total,
    SUM(CASE WHEN Placement_Status='Placed' THEN 1 ELSE 0 END) AS Placed,
    ROUND(SUM(CASE WHEN Placement_Status='Placed' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 1) AS Placement_Pct
FROM placements
GROUP BY Communication_Score
ORDER BY Communication_Score;
SELECT Student_ID, Gender, Stream, Cgpa, Communication_Score
FROM placements
WHERE Placement_Status = 'Not Placed'
AND Backlog = 'Yes'
AND Innovative_Project = 'No'
AND Technical_Course = 'No'
ORDER BY Cgpa ASC;
SELECT Internship,
    COUNT(*) AS Total,
    SUM(CASE WHEN Placement_Status='Placed' THEN 1 ELSE 0 END) AS Placed,
    ROUND(SUM(CASE WHEN Placement_Status='Placed' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 1) AS Placement_Pct
FROM placements
GROUP BY Internship;