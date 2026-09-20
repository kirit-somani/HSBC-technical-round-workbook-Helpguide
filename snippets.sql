--@@ schema
CREATE TABLE departments (
    id   INTEGER PRIMARY KEY,
    name TEXT
);
CREATE TABLE employees (
    id            INTEGER PRIMARY KEY,
    name          TEXT,
    salary        INTEGER,
    department_id INTEGER,
    manager_id    INTEGER
);
CREATE TABLE customers (
    id   INTEGER PRIMARY KEY,
    name TEXT
);
CREATE TABLE orders (
    id          INTEGER PRIMARY KEY,
    customer_id INTEGER,
    amount      INTEGER
);

INSERT INTO departments VALUES (1, 'Engineering'), (2, 'Operations'), (3, 'Finance'), (4, 'Legal');
INSERT INTO employees VALUES
    (1, 'Asha',   90000, 1, NULL),
    (2, 'Rahul',  70000, 1, 1),
    (3, 'Meera',  95000, 1, 1),
    (4, 'Karan',  50000, 2, NULL),
    (5, 'Sana',   50000, 2, 4),
    (6, 'Vikram', 60000, 3, NULL),
    (7, 'Neha',   60000, 3, 6),
    (8, 'Arjun',  45000, 2, 4);
INSERT INTO customers VALUES (1, 'Amit'), (2, 'Bhavna'), (3, 'Chirag');
INSERT INTO orders VALUES (1, 1, 500), (2, 1, 300), (3, 3, 700);
--@@ q_above_avg
SELECT name, salary
FROM employees
WHERE salary > (SELECT AVG(salary) FROM employees);
--@@ q_second_highest
SELECT MAX(salary) AS second_highest
FROM employees
WHERE salary < (SELECT MAX(salary) FROM employees);
--@@ q_nth_highest
SELECT DISTINCT salary
FROM employees
ORDER BY salary DESC
LIMIT 1 OFFSET 2;          -- OFFSET is N-1, so this is the 3rd highest
--@@ q_dense_rank
SELECT DISTINCT salary
FROM (
    SELECT salary, DENSE_RANK() OVER (ORDER BY salary DESC) AS rnk
    FROM employees
) AS ranked
WHERE rnk = 2;
--@@ q_dup_salary
SELECT salary, COUNT(*) AS how_many
FROM employees
GROUP BY salary
HAVING COUNT(*) > 1;
--@@ q_manager
SELECT e.name AS employee, e.salary, m.name AS manager, m.salary AS manager_salary
FROM employees e
JOIN employees m ON e.manager_id = m.id
WHERE e.salary > m.salary;
--@@ q_never_ordered
SELECT c.name
FROM customers c
LEFT JOIN orders o ON o.customer_id = c.id
WHERE o.id IS NULL;
--@@ q_dept_max
SELECT d.name AS department, e.name, e.salary
FROM employees e
JOIN departments d ON e.department_id = d.id
WHERE e.salary = (
    SELECT MAX(salary)
    FROM employees
    WHERE department_id = e.department_id
)
ORDER BY d.name, e.name;
--@@ q_headcount_having
SELECT d.name, COUNT(*) AS headcount
FROM employees e
JOIN departments d ON e.department_id = d.id
GROUP BY d.name
HAVING COUNT(*) > 2;
--@@ q_dept_left
SELECT d.name, COUNT(e.id) AS headcount, COALESCE(SUM(e.salary), 0) AS payroll
FROM departments d
LEFT JOIN employees e ON e.department_id = d.id
GROUP BY d.name
ORDER BY payroll DESC;
--@@ q_window_rank
SELECT name, department_id, salary,
       RANK() OVER (PARTITION BY department_id ORDER BY salary DESC) AS rnk
FROM employees;
--@@ q_customer_totals
SELECT c.name, SUM(o.amount) AS total_spent
FROM customers c
JOIN orders o ON o.customer_id = c.id
GROUP BY c.name
ORDER BY total_spent DESC;
--@@ tx_transfer
BEGIN;
UPDATE accounts SET balance = balance - 500 WHERE id = 1;
UPDATE accounts SET balance = balance + 500 WHERE id = 2;
COMMIT;          -- or ROLLBACK; if anything failed in between
--@@ index_example
CREATE INDEX idx_employees_salary ON employees(salary);
