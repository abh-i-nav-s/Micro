-- 3. Display the emp_no and name of employees from department no 'D02'
SELECT emp_no, emp_name
FROM Employee
WHERE dept_no = 'D02';


-- 4. Display emp_no, emp_name, designation, dept_no and salary 
-- of employees in the descending order of salary
SELECT emp_no, emp_name, designation, dept_no, salary
FROM Employee
ORDER BY salary DESC;


-- 5. Display the emp_no and name of employees whose salary is between 2000 and 5000
SELECT emp_no, emp_name
FROM Employee
WHERE salary BETWEEN 2000 AND 5000;


-- 6. Display the designations without duplicate values
SELECT DISTINCT designation
FROM Employee;


-- 7. Change the salary of employees to 45000 whose designation is 'Manager'
UPDATE Employee
SET salary = 45000
WHERE designation = 'Manager';


-- 8. Change the mobile number of employees named John
UPDATE Employee
SET mobile_no = 9999999999
WHERE emp_name = 'John';


-- 9. Delete all employees whose salary is equal to Rs.7000
DELETE FROM Employee
WHERE salary = 7000;


-- 10. Retrieve the name and mobile number of all employees whose name starts with 'A'
SELECT emp_name, mobile_no
FROM Employee
WHERE emp_name LIKE 'A%';


-- 11. Display the details of the employee whose name has at least three characters
-- and salary greater than 20000
SELECT *
FROM Employee
WHERE emp_name LIKE '___%' 
AND salary > 20000;


-- 12. Display the details of employees with empid 'emp01', 'emp02' and 'emp06'
SELECT *
FROM Employee
WHERE emp_no IN ('emp01','emp02','emp06');


-- 13. Display employee name and employee id of those who have salary 
-- between 120000 and 300000
SELECT emp_name, emp_no
FROM Employee
WHERE salary BETWEEN 120000 AND 300000;


-- 14. Display the details of employees whose designation 
-- is 'Manager' or 'Computer Assistant'
SELECT *
FROM Employee
WHERE designation = 'Manager'
OR designation = 'Computer Assistant';


-- 15. Display how many employees work for each department
SELECT dept_no, COUNT(*) AS total_employees
FROM Employee
GROUP BY dept_no;


-- 16. Display average salary of employees in each department
SELECT dept_no, AVG(salary) AS average_salary
FROM Employee
GROUP BY dept_no;


-- 17. Display total salary of employees in each department
SELECT dept_no, SUM(salary) AS total_salary
FROM Employee
GROUP BY dept_no;


-- 18. Display top and lower salary of employees in each department
SELECT dept_no, MAX(salary) AS highest_salary, MIN(salary) AS lowest_salary
FROM Employee
GROUP BY dept_no;


-- 19. Display average salary of employees in all departments 
-- except department with department number 'D05'
SELECT dept_no, AVG(salary) AS average_salary
FROM Employee
WHERE dept_no <> 'D05'
GROUP BY dept_no;


-- 20. Display average salary of employees in all departments except 'D01'
-- and average salary greater than 20000 in ascending order
SELECT dept_no, AVG(salary) AS average_salary
FROM Employee
WHERE dept_no <> 'D01'
GROUP BY dept_no
HAVING AVG(salary) > 20000
ORDER BY average_salary ASC;
