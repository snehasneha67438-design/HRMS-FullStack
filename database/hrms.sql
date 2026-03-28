CREATE DATABASE hrms_db;
USE hrms_db;

CREATE TABLE employees (
    emp_id INT AUTO_INCREMENT PRIMARY KEY,
    emp_name VARCHAR(100),
    email VARCHAR(100),
    phone VARCHAR(15),
    department VARCHAR(50),
    designation VARCHAR(50),
    salary DECIMAL(10,2)
);

SHOW TABLES;
SELECT * FROM employees;

CREATE TABLE attendance (
    att_id INT AUTO_INCREMENT PRIMARY KEY,
    emp_id INT,
    emp_name VARCHAR(100),
    attendance_date DATE,
    clock_in TIME,
    clock_out TIME,
    status VARCHAR(20)
);

SELECT * FROM attendance;

CREATE TABLE leaves (
    leave_id INT AUTO_INCREMENT PRIMARY KEY,
    emp_id INT,
    emp_name VARCHAR(100),
    leave_type VARCHAR(50),
    from_date DATE,
    to_date DATE,
    reason VARCHAR(255),
    status VARCHAR(20)
);

SELECT * FROM leaves;

CREATE TABLE payroll (
    payroll_id INT AUTO_INCREMENT PRIMARY KEY,
    emp_id INT,
    emp_name VARCHAR(100),
    basic_salary DECIMAL(10,2),
    tax DECIMAL(10,2),
    bonus DECIMAL(10,2),
    net_salary DECIMAL(10,2),
    month VARCHAR(20)
);

SELECT * FROM payroll;