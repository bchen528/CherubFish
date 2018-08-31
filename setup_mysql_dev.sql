-- prepares a MySQL server for the project
CREATE DATABASE IF NOT EXISTS `commando`;
CREATE USER IF NOT EXISTS 'cherubfish'@'localhost' IDENTIFIED BY 'cherubpassword';
GRANT USAGE ON *.* TO 'cherubfish'@'localhost';
GRANT SELECT ON `performance_schema`.* TO 'cherubfish'@'localhost';
GRANT ALL PRIVILEGES ON `commando`.* TO 'cherubfish'@'localhost';
FLUSH PRIVILEGES;
