DELIMITER $$
DROP PROCEDURE IF EXISTS SP_ADDUserDetails $$
CREATE PROCEDURE SP_ADDUserDetails(
IN emailId VARCHAR(255),
IN FN VARCHAR(255),
IN LN VARCHAR(255),
IN typeId int

)
BEGIN 
	DECLARE userid INT;

   
	INSERT INTO Users(  User_Type_id, First_name, Last_name, Email) 
    VALUES (typeId, FN,LN, emailId );   
				
   
END$$

DELIMITER ;