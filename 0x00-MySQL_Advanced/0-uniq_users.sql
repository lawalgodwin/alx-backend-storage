-- Write a SQL script that creates a table users
-- Attributes requirements:
--  id, integer, never null, auto increment and primary key
--  email, string (255 characters), never null and unique
--  name, string (255 characters)

CREATE TABLE IF NOT EXISTS users (
  id INT AUTO_INCREMENT NOT NULL,
  email VARCHAR(255) NOT NULL UNIQUE,
  name VARCHAR(255),
  PRIMARY KEY(id)
  );
