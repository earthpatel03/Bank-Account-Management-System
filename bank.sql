CREATE DATABASE IF NOT EXISTS bank_db;
USE bank_db;

CREATE TABLE accounts (
    acc_no INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100),
    balance DECIMAL(10,2) DEFAULT 0,
    last_interest_date DATE
);

CREATE TABLE transactions (
    txn_id INT PRIMARY KEY AUTO_INCREMENT,
    acc_no INT,
    type VARCHAR(20),
    amount DECIMAL(10,2),
    txn_time DATETIME,
    FOREIGN KEY (acc_no) REFERENCES accounts(acc_no)
);

select * from accounts;

select * from transactions;