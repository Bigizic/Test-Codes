-- prepares the database and user
CREATE DATABASE IF NOT EXISTS ElectricVehicle;
CREATE USER IF NOT EXISTS 'user_1738'@'localhost' IDENTIFIED BY 'groot';
GRANT ALL PRIVILEGES ON ElectricVehicle . * TO 'user_1738'@'localhost';
GRANT SELECT ON performance_schema . * TO 'user_1738'@'localhost';
