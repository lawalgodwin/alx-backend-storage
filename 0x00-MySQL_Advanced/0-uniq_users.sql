-- Write a SQL script that creates a table users
CREATE TABLE IF NOT EXISTS users (
  id INT AUTO_INCREMENT NOT NULL,
  email UNIQUE VARCHAR(255) NOT NULL,
  name VARCHAR(255),
  PRIMARY KEY(id)
  );
