DELIMITER $$
DROP PROCEDURE IF EXISTS SP_GetWrittenBlogs $$
CREATE PROCEDURE SP_GetWrittenBlogs(
IN userId varchar(255)
)
BEGIN
	SELECT b.Blog_id, b.blog_title, b.blog_description, b.image_link, b.Thumbnail FROM Blogs b left join WrittenBlogs wb on b.Blog_id = wb.blog_id where  wb.user_id =  userId;
   
END$$

DELIMITER ;