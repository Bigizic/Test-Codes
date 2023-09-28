-- prepares a database to store the url records

CREATE DATABASE IF NOT EXISTS Izy_url;
USE Izy_url;
CREATE TABLE IF NOT EXISTS Easy_URLS (
	Id INT PRIMARY KEY,
	Original_url VARCHAR(500) NOT NULL,
	easy_url VARCHAR(10) NOT NULL
);
