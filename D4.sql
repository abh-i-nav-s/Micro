-- 1. Create table regions
CREATE TABLE regions (
    region_id INT PRIMARY KEY,
    region_name VARCHAR(50)
);

-- 2. Create table countries
CREATE TABLE countries (
    country_id CHAR(2) PRIMARY KEY,
    country_name VARCHAR(50),
    region_id INT,
    FOREIGN KEY (region_id) REFERENCES regions(region_id)
);

-- 3. Create table locations
CREATE TABLE locations (
    location_id INT PRIMARY KEY,
    street_address VARCHAR(100),
    postal_code VARCHAR(20),
    city VARCHAR(50),
    state_province VARCHAR(50),
    country_id CHAR(2),
    FOREIGN KEY (country_id) REFERENCES countries(country_id)
);

-- 4. Create table departments
CREATE TABLE departments (
    department_id INT PRIMARY KEY,
    department_name VARCHAR(50),
    location_id INT,
    FOREIGN KEY (location_id) REFERENCES locations(location_id)
);

-- 7. Create table jobs
CREATE TABLE jobs (
    job_id VARCHAR(10) PRIMARY KEY,
    job_title VARCHAR(50),
    min_salary DECIMAL(10,2),
    max_salary DECIMAL(10,2)
);

-- 5. Create table employees
CREATE TABLE employees (
    employee_id INT PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    email VARCHAR(100),
    phone_number VARCHAR(20),
    hire_date DATE,
    job_id VARCHAR(10),
    salary DECIMAL(10,2),
    manager_id INT,
    department_id INT,
    FOREIGN KEY (job_id) REFERENCES jobs(job_id),
    FOREIGN KEY (manager_id) REFERENCES employees(employee_id),
    FOREIGN KEY (department_id) REFERENCES departments(department_id)
);

-- 6. Create table dependents
CREATE TABLE dependents (
    dependent_id INT PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    relationship VARCHAR(50),
    employee_id INT,
    FOREIGN KEY (employee_id) REFERENCES employees(employee_id)
);

-- 8. Insert into regions
INSERT INTO regions VALUES
(1, 'Europe'),
(2, 'Americas'),
(3, 'Asia'),
(4, 'Middle East and Africa');

-- 9. Insert into countries
INSERT INTO countries VALUES
('IT', 'Italy', 1),
('US', 'United States', 2),
('JP', 'Japan', 3),
('IN', 'India', 3),
('ZA', 'South Africa', 4);

-- 10. Insert into locations
INSERT INTO locations VALUES
(1000, 'Via Roma 100', '00100', 'Rome', 'Lazio', 'IT'),
(1700, '200 Broadway', '94111', 'San Francisco', 'California', 'US'),
(1800, 'Nishi Shinjuku 3-2', '160-0023', 'Tokyo', 'Tokyo', 'JP'),
(1900, 'Block B, ITPL', '560066', 'Bangalore', 'Karnataka', 'IN'),
(2000, '1 Mandela Way', '8001', 'Cape Town', 'Western Cape', 'ZA'),
(2100, '123 Connaught Place', '110001', 'Delhi', 'Delhi', 'IN');

-- 11. Insert into departments
INSERT INTO departments VALUES
(10, 'Administration', 1000),
(20, 'Marketing', 1700),
(30, 'Sales', 1700),
(40, 'Finance', 1800),
(50, 'IT', 1900);

-- 14. Insert into jobs
INSERT INTO jobs VALUES
('J01', 'Administrator', 10000, 15000),
('J02', 'Marketing Specialist', 7000, 12000),
('J03', 'Sales Manager', 12000, 18000),
('J04', 'Finance Analyst', 10000, 14000),
('J05', 'IT Specialist', 9000, 13000);

-- 12. Insert into employees
INSERT INTO employees VALUES
(101, 'John', 'Doe', 'jdoe@example.com', '1234567890', '2020-01-15', 'J01', 12000, NULL, 10),
(102, 'Jane', 'Smith', 'jsmith@example.com', '9876543210', '2019-03-10', 'J02', 8000, 101, 20),
(103, 'Alice', 'Johnson', 'ajohnson@example.com', '5556667777', '2018-11-25', 'J03', 15000, 101, 30),
(104, 'Robert', 'Taylor', 'rtaylor@example.com', '8889990000', '2021-07-01', 'J04', 11000, 102, 40),
(105, 'Linda', 'Williams', 'lwilliams@example.com', '4445556666', '2022-05-12', 'J05', 9500, 103, 50),
(106, 'Mark', 'Brown', 'mbrown@example.com', '9998887777', '2024-01-10', 'J05', 11000, 105, 50),
(109, 'Zara', 'Ali', 'zali@example.com', '3334445555', '2024-02-01', 'J01', 9000, NULL, 10),
(110, 'Ravi', 'Sharma', 'rsharma@example.com', '9998887777', '2024-03-15', 'J01', 8500, NULL, 20),
(111, 'Smith', 'David', 'dsmith@example.com', '8887776666', '2024-04-01', 'J03', NULL, NULL, 40);

-- 13. Insert into dependents
INSERT INTO dependents VALUES
(1, 'Anna', 'Doe', 'Daughter', 101),
(2, 'Michael', 'Smith', 'Son', 102),
(3, 'Emily', 'Johnson', 'Spouse', 103),
(4, 'Sophia', 'Taylor', 'Daughter', 104),
(5, 'James', 'Williams', 'Son', 105);

-- 15. Display all records
SELECT * FROM regions;
SELECT * FROM countries;
SELECT * FROM locations;
SELECT * FROM departments;
SELECT * FROM employees;
SELECT * FROM dependents;
SELECT * FROM jobs;

-- 16. Employees in location 1700
SELECT e.* FROM employees e
JOIN departments d ON e.department_id = d.department_id
WHERE d.location_id = 1700;

-- 17. Employees not in location 1700
SELECT e.* FROM employees e
JOIN departments d ON e.department_id = d.department_id
WHERE d.location_id <> 1700;

-- 18. Highest salary employees
SELECT * FROM employees
WHERE salary = (SELECT MAX(salary) FROM employees);

-- 19. Salary > average
SELECT * FROM employees
WHERE salary > (SELECT AVG(salary) FROM employees);

-- 20. Departments with salary > 10000
SELECT DISTINCT d.department_id, d.department_name
FROM departments d
WHERE d.department_id IN (
    SELECT department_id FROM employees WHERE salary > 10000
);

-- 21. Departments without salary > 10000
SELECT d.department_id, d.department_name
FROM departments d
WHERE d.department_id NOT IN (
    SELECT department_id FROM employees WHERE salary > 10000
);

-- 22. Salary > min in department
SELECT * FROM employees e
WHERE salary > (
    SELECT MIN(salary) FROM employees WHERE department_id = e.department_id
);

-- 23. Salary >= max in department
SELECT * FROM employees e
WHERE salary >= (
    SELECT MAX(salary) FROM employees WHERE department_id = e.department_id
);

-- 24. Avg salary per department
SELECT department_id, AVG(salary)
FROM employees
GROUP BY department_id;

-- 25. Salary, avg, difference
SELECT employee_id, first_name, salary,
(SELECT AVG(salary) FROM employees),
salary - (SELECT AVG(salary) FROM employees)
FROM employees;

-- 26. Salary > dept avg
SELECT * FROM employees e
WHERE salary > (
    SELECT AVG(salary) FROM employees WHERE department_id = e.department_id
);

-- 27. No dependents
SELECT * FROM employees
WHERE employee_id NOT IN (SELECT employee_id FROM dependents);

-- 28. Dept 1,2,3 employees
SELECT first_name, last_name, department_id
FROM employees
WHERE department_id IN (1,2,3);

-- 29. Employee + job + dept
SELECT e.first_name, e.last_name, j.job_title, d.department_name
FROM employees e
JOIN jobs j ON e.job_id = j.job_id
JOIN departments d ON e.department_id = d.department_id
WHERE e.salary > 10000 AND e.department_id IN (10,20,30);

-- 30. Dept + location + country + region
SELECT d.department_name, l.street_address, l.postal_code, c.country_name, r.region_name
FROM departments d
JOIN locations l ON d.location_id = l.location_id
JOIN countries c ON l.country_id = c.country_id
JOIN regions r ON c.region_id = r.region_id;

-- 31. Employees with/without department
SELECT e.first_name, e.last_name, e.department_id, d.department_name
FROM employees e LEFT JOIN departments d ON e.department_id = d.department_id;

-- 32. First name contains Z
SELECT e.first_name, e.last_name, d.department_name, l.city, l.state_province
FROM employees e
JOIN departments d ON e.department_id = d.department_id
JOIN locations l ON d.location_id = l.location_id
WHERE e.first_name LIKE '%Z%';

-- 33. All departments including no employees
SELECT e.first_name, e.last_name, d.department_id, d.department_name
FROM departments d LEFT JOIN employees e ON e.department_id = d.department_id;

-- 34. Employee and manager
SELECT e.first_name, m.first_name
FROM employees e LEFT JOIN employees m ON e.manager_id = m.employee_id;

-- 35. Same dept as Taylor
SELECT first_name, last_name, department_id
FROM employees
WHERE department_id = (SELECT department_id FROM employees WHERE last_name='Taylor');

-- 36. Salary difference
SELECT j.job_title, e.first_name, (j.max_salary - e.salary)
FROM employees e JOIN jobs j ON e.job_id = j.job_id;

-- 37. Avg salary and count
SELECT d.department_name, AVG(e.salary), COUNT(e.employee_id)
FROM departments d LEFT JOIN employees e ON d.department_id = e.department_id
GROUP BY d.department_name;

-- 38. Create view for Delhi
CREATE VIEW emp_view_delhi AS
SELECT e.employee_id, e.first_name, e.phone_number, j.job_title, d.department_name, m.first_name
FROM employees e
JOIN jobs j ON e.job_id = j.job_id
JOIN departments d ON e.department_id = d.department_id
JOIN locations l ON d.location_id = l.location_id
LEFT JOIN employees m ON e.manager_id = m.employee_id
WHERE l.city = 'Delhi';

-- 39. Query from view
SELECT * FROM emp_view_delhi
WHERE job_title LIKE '%Manager%' AND department_name='Finance';

-- 40. (Conceptual – Not updatable view)

-- 41. Employees with no dependents
SELECT * FROM employees
WHERE employee_id NOT IN (SELECT employee_id FROM dependents);

-- 42. Manager 101 or 201
SELECT * FROM employees WHERE manager_id = 101
UNION
SELECT * FROM employees WHERE manager_id = 201;

-- 43. Employees with dependents
SELECT * FROM employees
WHERE employee_id IN (SELECT employee_id FROM dependents);
