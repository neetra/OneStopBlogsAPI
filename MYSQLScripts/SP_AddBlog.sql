DELIMITER $$
DROP PROCEDURE IF EXISTS SP_AddBlog $$
CREATE PROCEDURE SP_AddBlog(
IN userId varchar(255),
IN blogTitle tinytext,
IN blogDescription mediumtext,
IN imageLink varchar(255),
IN thumbNail  varchar(255)

)
BEGIN 
	DECLARE blogId varchar(255);
	
	SET @blogId = UUID_SHORT();
	

	INSERT INTO Blogs( Blog_id, blog_title, blog_description, image_link, Thumbnail) 
	VALUES (@blogId,blogTitle, blogDescription,imageLink, thumbNail );   
    
    INSERT into WrittenBlogs(Blog_id, user_id) Values (@blogId,userId );
    SELECT * FROM Blogs where Blog_id = @blogId LIMIT 1;			
				
   
END$$

DELIMITER ;