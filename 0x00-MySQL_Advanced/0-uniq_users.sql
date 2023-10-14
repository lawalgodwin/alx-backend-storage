-- Write a SQL script that creates a table users
-- create the table only if not exists
-- Requirement:
--   id, integer, never null, auto increment and primary key
--   email, string (255 characters), never null and unique
--   name, string (255 characters)
CREATE TABLE IF NOT EXISTS users (
  id INT AUTO_INCREMENT NOT NULL,
  email UNIQUE VARCHAR(255) NOT NULL,
  name VARCHAR(255),
  PRIMARY KEY(id)
  );
