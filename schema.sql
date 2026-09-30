CREATE DATABASE IF NOT EXISTS budgetai CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE budgetai;

CREATE TABLE IF NOT EXISTS accounts (
 id INT AUTO_INCREMENT PRIMARY KEY,
 name VARCHAR(100) NOT NULL UNIQUE,
 type VARCHAR(30) NOT NULL DEFAULT 'cash',
 currency VARCHAR(10) NOT NULL DEFAULT 'MAD',
 opening_balance DECIMAL(15,2) NOT NULL DEFAULT 0,
 active TINYINT(1) NOT NULL DEFAULT 1
);

CREATE TABLE IF NOT EXISTS categories (
 id INT AUTO_INCREMENT PRIMARY KEY,
 name VARCHAR(100) NOT NULL UNIQUE,
 parent_id INT NULL,
 kind VARCHAR(20) NOT NULL DEFAULT 'expense',
 FOREIGN KEY(parent_id) REFERENCES categories(id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS transactions (
 id BIGINT AUTO_INCREMENT PRIMARY KEY,
 kind ENUM('income','expense','transfer') NOT NULL,
 amount DECIMAL(15,2) NOT NULL,
 currency VARCHAR(10) NOT NULL,
 category VARCHAR(100) NOT NULL,
 account VARCHAR(100) NOT NULL DEFAULT 'Cash',
 merchant VARCHAR(150) DEFAULT '',
 note TEXT,
 date DATE NOT NULL,
 recurring_id BIGINT NULL,
 INDEX idx_tx_date(date),
 INDEX idx_tx_category(category)
);

CREATE TABLE IF NOT EXISTS budgets (
 id BIGINT AUTO_INCREMENT PRIMARY KEY,
 category VARCHAR(100) NOT NULL,
 amount DECIMAL(15,2) NOT NULL,
 currency VARCHAR(10) NOT NULL,
 period VARCHAR(20) NOT NULL DEFAULT 'monthly',
 month CHAR(7) NOT NULL,
 UNIQUE KEY uq_budget(category,currency,period,month)
);

CREATE TABLE IF NOT EXISTS recurring_transactions (
 id BIGINT AUTO_INCREMENT PRIMARY KEY,
 kind ENUM('income','expense') NOT NULL,
 amount DECIMAL(15,2) NOT NULL,
 currency VARCHAR(10) NOT NULL,
 category VARCHAR(100) NOT NULL,
 account VARCHAR(100) NOT NULL DEFAULT 'Cash',
 description VARCHAR(255) DEFAULT '',
 frequency VARCHAR(20) NOT NULL DEFAULT 'monthly',
 next_date DATE NOT NULL,
 active TINYINT(1) NOT NULL DEFAULT 1
);

CREATE TABLE IF NOT EXISTS goals (
 id BIGINT AUTO_INCREMENT PRIMARY KEY,
 name VARCHAR(120) NOT NULL UNIQUE,
 target DECIMAL(15,2) NOT NULL,
 saved DECIMAL(15,2) NOT NULL DEFAULT 0,
 currency VARCHAR(10) NOT NULL DEFAULT 'MAD',
 deadline DATE NULL,
 note TEXT
);

INSERT IGNORE INTO accounts(name,type,currency) VALUES ('Cash','cash','MAD');
INSERT IGNORE INTO categories(name,kind) VALUES
('Food','expense'),('Housing','expense'),('Transport','expense'),
('Utilities','expense'),('Shopping','expense'),('Health','expense'),
('Entertainment','expense'),('Education','expense'),('Travel','expense'),
('Subscriptions','expense'),('Other','expense');
