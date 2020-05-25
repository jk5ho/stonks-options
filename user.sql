CREATE DATABASE IF NOT EXISTS project_stonk;
CREATE USER IF NOT EXISTS 'hobin'@'localhost' IDENTIFIED BY 'rood';
GRANT ALL PRIVILEGES ON project_stonk.* TO 'hobin'@'localhost';