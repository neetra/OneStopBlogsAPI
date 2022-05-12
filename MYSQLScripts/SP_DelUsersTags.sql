DELIMITER $$
DROP PROCEDURE IF EXISTS SP_DelUsersTags $$
CREATE PROCEDURE SP_DelUsersTags(
IN tagName VARCHAR(255),
IN userId VARCHAR(255)
)
BEGIN 
	DECLARE tagid INT;
	select tag_id into @tagid  from tags  where tag_name = tagName LIMIT 1;
 
	DELETE FROM UsersTags  WHERE user_id = userId and tag_id = @tagid ;
    select t.tag_id, t.tag_name from UsersTags ut left join tags t on t.tag_id = ut.tag_id where ut.user_id = userId;	
				
   
END$$

DELIMITER ;