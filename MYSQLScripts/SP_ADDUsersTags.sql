DELIMITER $$
DROP PROCEDURE IF EXISTS SP_AddUsersTags $$
CREATE PROCEDURE SP_AddUsersTags(
IN tagName VARCHAR(255),
IN userId VARCHAR(255)
)
BEGIN 
	DECLARE tagid INT;
	select tag_id into @tagid  from tags  where tag_name = tagName LIMIT 1;

	INSERT INTO UsersTags( user_id,tag_id) 
	VALUES (userId, @tagid  );   
    		
				
   
END$$

DELIMITER ;