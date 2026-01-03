-- MySQL Database Setup Script
-- Creates database and user for File Explorer Notes System

-- Create the database
CREATE DATABASE IF NOT EXISTS file_explorer_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Create user with password '0000'
CREATE USER IF NOT EXISTS 'file_explorer_user'@'localhost' IDENTIFIED BY 'PASSWORD_password_0000';

-- Grant all privileges on the database to the user
GRANT ALL PRIVILEGES ON file_explorer_db.* TO 'file_explorer_user'@'localhost';

-- Grant privileges for creating tables and other operations
GRANT CREATE, DROP, ALTER, INSERT, UPDATE, DELETE, SELECT, INDEX ON file_explorer_db.* TO 'file_explorer_user'@'localhost';

-- Flush privileges to apply changes
FLUSH PRIVILEGES;

-- Use the database
USE file_explorer_db;

-- Create notes table
CREATE TABLE IF NOT EXISTS notes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL DEFAULT '',
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_created_at (created_at),
    INDEX idx_updated_at (updated_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Create users table for passkey authentication
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL UNIQUE,
    passkey VARCHAR(255) NOT NULL,
    has_passkey BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_username (username),
    INDEX idx_has_passkey (has_passkey)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Show success message
SELECT 'Database and user created successfully!' AS message;
SELECT 'Database: file_explorer_db' AS database_name;
SELECT 'User: file_explorer_user' AS username;

