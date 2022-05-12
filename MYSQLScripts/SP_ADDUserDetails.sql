DELIMITER $$
DROP PROCEDURE IF EXISTS SP_ADDUserDetails $$
CREATE PROCEDURE SP_ADDUserDetails(
IN emailId VARCHAR(255),
IN FN VARCHAR(255),
IN LN VARCHAR(255),
IN typeId int,
IN userId VARCHAR(255)
)
BEGIN 
	DECLARE user_id varchar(255);
	IF userId IS NULL THEN  
		SET @user_id = UUID_SHORT();
	else
		SET @user_id = userId;
    END IF;

	INSERT INTO Users( User_id, User_Type_id, First_name, Last_name, Email) 
	VALUES (@user_id,typeId, FN,LN, emailId );   
    SELECT * FROM Users where User_id = @user_id LIMIT 1;			
				
   
END$$

DELIMITER ;