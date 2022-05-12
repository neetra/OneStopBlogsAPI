-- -----------------------------------------------------
-- Table `onestopblogs`.`Users`
-- -----------------------------------------------------

CREATE TABLE IF NOT EXISTS `onestopblogs`.`UsersTypes` ( 
  `Type_id` int not null,
  `description` VARCHAR(100) NULL,
    PRIMARY KEY (`Type_id`)
  );
  
CREATE TABLE IF NOT EXISTS `onestopblogs`.`Users` (
  `User_id` INT NOT NULL AUTO_INCREMENT,
  `User_Type_id` int default 0,
  `First_name` VARCHAR(50) NULL,
  `Last_name` VARCHAR(100) NULL,
  `Email` VARCHAR(255) NOT NULL,  
  PRIMARY KEY (`User_id`),
  UNIQUE INDEX `Email_UNIQUE` (`Email` ASC),
    CONSTRAINT `fk_users_type`
    FOREIGN KEY (`User_Type_id`)
    REFERENCES `onestopblogs`.`UsersTypes` (`Type_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
);

alter table Users modify column user_id varchar(255);



CREATE TABLE IF NOT EXISTS `onestopblogs`.`tags` (
  `tag_id` INT NOT NULL AUTO_INCREMENT,
  `tag_name` VARCHAR(255) not null,
    
  PRIMARY KEY (`tag_id`),
  UNIQUE INDEX `tag_name` (`tag_name` ASC)
);

CREATE TABLE IF NOT EXISTS `onestopblogs`.`UsersTags` (
  `tag_id` INT NOT NULL,
  `user_id` varchar(255),     
    FOREIGN KEY (`tag_id`)
    REFERENCES `onestopblogs`.`tags` (`tag_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
   
);

alter table UsersTags add constraint foreign key (user_id) REFERENCES Users(user_id);

CREATE TABLE IF NOT EXISTS `onestopblogs`.`Blogs` (
  `Blog_id` INT NOT NULL AUTO_INCREMENT,
  `blog_title` tinytext not null,
   `blog_description` mediumtext not null, 
    `image_link` varchar(255) , 
     `Thumbnail` varchar(255) , 
  PRIMARY KEY (`Blog_id`)
);

alter table Blogs modify Blog_id varchar(255);

CREATE TABLE IF NOT EXISTS `onestopblogs`.`WrittenBlogs` (
  `blog_id` varchar(255) not null,
  `user_id` varchar(255) not null,
	Primary key ( `user_id`,   `blog_id` ),
   FOREIGN KEY (`Blog_id`)
REFERENCES `onestopblogs`.`Blogs` (`Blog_id`),
   FOREIGN KEY (`user_id`)
REFERENCES `onestopblogs`.`Users` (`user_id`)

);






