-- Write a SQL script that creates a stored procedure AddBonus that
-- adds a new correction for a student.
-- Requirements:
--   Procedure AddBonus is taking 3 inputs (in this order):
--     user_id, a users.id value (you can assume user_id is linked to an existing users)
--     project_name, a new or already exists projects -
--     if no projects.name found in the table, you should create it
--     score, the score value for the correction
--     Context: Write code in SQL is a nice level up!
DELIMITER $$

CREATE PROCEDURE AddBonus(IN user_id INT, IN project_name VARCHAR(255), IN score INT)
BEGIN
  DECLARE projectId INT;
  DECLARE projectExists INT;
  -- check if the project exists and create accordingly
  SELECT COUNT(*) INTO projectExists FROM projects WHERE projects.name=project_name;
  -- if the project does not exist, create it
  IF projectExists = 0 THEN
    INSERT INTO projects (name) VALUES (project_name);
    SET projectId = LAST_INSERT_ID();
  ELSE
    SELECT id INTO projectId FROM projects WHERE projects.name=project_name;
  END IF;
  -- Add correction for a student
  INSERT INTO corrections (user_id, project_id, score)
  VALUES (user_id, projectId, score);
END $$
DELIMITER ;$$
