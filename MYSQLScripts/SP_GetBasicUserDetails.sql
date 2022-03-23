DELIMITER $$
DROP PROCEDURE IF EXISTS SP_GetBasicUserDetails $$
CREATE PROCEDURE SP_GetBasicUserDetails(
IN emailId VARCHAR(255),
IN userId int
)
BEGIN
	SELECT u.user_id as userId,  u.email as Email , u.first_name as firstName, u.last_name as lastName, u.user_type_id as typeId, ut.description as type FROM Users u 
    LEFT JOIN UsersTypes ut ON u.user_type_id = ut.Type_id  
    WHERE u.email = emailId or u.user_id = userId;
   
END$$

DELIMITER ;