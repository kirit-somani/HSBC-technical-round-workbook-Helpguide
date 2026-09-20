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