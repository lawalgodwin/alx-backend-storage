-- Write a SQL script that creates a stored procedure ComputeAverageScoreForUser
-- that computes and store the average score for a student.
-- Note: An average score can be a decimal

-- Requirements:
--    Procedure ComputeAverageScoreForUser is taking 1 input:
--    user_id, a users.id value (you can assume user_id is linked to an existing users)

DELIMITER $$

CREATE PROCEDURE ComputeAverageScoreForUser (IN user_id INT)
BEGIN
  DECLARE average FLOAT;
  -- Get the average
  SELECT AVG(score) INTO average FROM corrections WHERE corrections.user_id=user_id;
  -- update students average score
  UPDATE users SET average_score = average WHERE users.id=user_id;
END $$
DELIMITER ;$$