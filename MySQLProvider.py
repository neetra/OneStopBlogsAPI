from configparser import Error
from tabnanny import check
from typing import Tuple
import mysql.connector 
from MySQLHelper import closeMysqlconnection, createConnection
from datetime import datetime
import config
from werkzeug.security import generate_password_hash, check_password_hash
from mysql.connector.cursor import MySQLCursorDict, MySQLCursorPrepared
import re

from Constants import JSONKeys
class MySQLProvider():   

    
 

 
# Make a regular expression
# for validating an Email

 
# Define a function for
# for validating an Email
 
 
    def check(self,email):
        try:
            regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        # pass the regular expression
        # and the string into the fullmatch() method
            if(re.fullmatch(regex, email)):
             return True;
    
            else:
                return False
        except Error as e:
            print(f"{e.message}")
            return False
        return False            
 

    def get_sql_version(self, oneStopBlogDbConnection= None):
        
        try:     
            oneStopBlogDbConnection = createConnection()        
           
            
            my_cursor = oneStopBlogDbConnection.cursor(dictionary = True)
            
            query = "SELECT version()"
        
            
            my_cursor.execute(query)
            
            results = my_cursor.fetchone()
            if(results is None):
                return None

                         
            return results["version()"]               
        except mysql.connector.Error as err:
            print (err)     
        finally:
            closeMysqlconnection(oneStopBlogDbConnection)                   
        
        return None
        
    
    def get_user_by_id_or_email(self, username, oneStopBlogDbConnection= None):
        try: 
            isEmail = self.check(str(username))
            oneStopBlogDbConnection = createConnection()     #established connection between your database   
            result =  None
            with oneStopBlogDbConnection.cursor() as my_cursor:
                if( isEmail):
                
                    my_cursor.callproc('SP_GetBasicUserDetails', (username,None)) 
                else:
                    my_cursor.callproc('SP_GetBasicUserDetails', (None,username))   


         
                result = my_cursor.fetchone()
              
           
            return result                
        except mysql.connector.Error as err:
            print (err)
        finally:
            closeMysqlconnection(oneStopBlogDbConnection)         
        
        return None

    def create_user(self, user_l):
        try: 
            
            oneStopBlogDbConnection = createConnection()     #established connection between your database   
            result =  None
            userId = None
            with oneStopBlogDbConnection.cursor() as my_cursor:     
                isAttrPresent = True if  "UserId" in user_l.keys() else False;
                if isAttrPresent:
                   userId = user_l[JSONKeys.USERID]
                my_cursor.callproc('SP_ADDUserDetails', (user_l[JSONKeys.EMAIL],user_l[JSONKeys.FIRSTNAME], user_l[JSONKeys.LASTNAME], user_l[JSONKeys.USERTYPE], userId)) 
                oneStopBlogDbConnection.commit()
                
                my_cursor.callproc('SP_GetBasicUserDetails', (user_l[JSONKeys.EMAIL], None))   
                result = my_cursor.fetchone()
                print(result)

            return result                
        except mysql.connector.Error as err:
            return err.msg
        except Error as e:
            return e
        finally:
            closeMysqlconnection(oneStopBlogDbConnection)         
        
        return None
    def get_tags(self, oneStopBlogDbConnection=None):
        try: 
            
            oneStopBlogDbConnection = createConnection()     #established connection between your database   
            result =  None            
            with oneStopBlogDbConnection.cursor() as my_cursor:     
                query = ("SELECT * from tags")

   
                my_cursor.execute(query)

                result = my_cursor.fetchall()
                print(result)

            return result                
        except mysql.connector.Error as err:
            return err.msg
        except Error as e:
            return e
        finally:
            closeMysqlconnection(oneStopBlogDbConnection)         
        
        return None
    def get_tag(self, tagName, oneStopBlogDbConnection=None):
        try: 
            
            oneStopBlogDbConnection = createConnection()     #established connection between your database   
            result =  None   

            with oneStopBlogDbConnection.cursor() as my_cursor:   
                if(not tagName.isdigit())  :
                    query = """SELECT * from tags where tag_name like %s"""

    
                    my_cursor.execute(query,("%" + tagName + "%"))

                    result = my_cursor.fetchall()
                else:
                    query = """SELECT * from tags where tag_id = %s"""

    
                    my_cursor.execute(query,( tagName ))

                    result = my_cursor.fetchall()                   
            
            return result                
        except mysql.connector.Error as err:
            return err.msg
        except Error as e:
            return e
        finally:
            closeMysqlconnection(oneStopBlogDbConnection)   

    def add_blog(self, blogData, userId, oneStopBlogDbConnection=None):
        try:
            oneStopBlogDbConnection = createConnection()     #established connection between your database   
            result =  None
            imageLink = None
            thumbnailLink = None
            with oneStopBlogDbConnection.cursor() as my_cursor:     
               
                if  "ImageLink" in blogData.keys():
                   imageLink = blogData[JSONKeys.IMAGELINK]

                if  JSONKeys.THUMBNAILlINK in blogData.keys():
                   thumbnailLink = blogData[JSONKeys.THUMBNAILlINK]                   
                my_cursor.callproc('SP_AddBlog', (userId, blogData[JSONKeys.BLOGTITLE],blogData[JSONKeys.BLOGDESCRIPTION], 
                                                    imageLink, thumbnailLink)) 
                oneStopBlogDbConnection.commit()               
                
                result = my_cursor.fetchone()
                print(result)

            return result                
        except mysql.connector.Error as err:
            return err.msg
        except Error as e:
            return e
        finally:
            closeMysqlconnection(oneStopBlogDbConnection)     

    def add_tags_for_user(self, tags,userId , oneStopBlogDbConnection=None):
        try:             
            oneStopBlogDbConnection = createConnection()     #established connection between your database   
            result =  None   

            with oneStopBlogDbConnection.cursor() as my_cursor:   
                for tagName in tags['tags']:
                   my_cursor.callproc('SP_AddUsersTags', (tagName, userId)) 
                   oneStopBlogDbConnection.commit() 

                query = """SELECT t.tag_id, t.tag_name from UsersTags ut LEFT JOIN tags t on ut.tag_id = t.tag_id where ut.user_id = %s"""

    
                my_cursor.execute(query,( userId))

                result = my_cursor.fetchall()                                
            
            print(result)
            return result                
        except mysql.connector.Error as err:
            return err.msg
        except Error as e:
            return e
        finally:
            closeMysqlconnection(oneStopBlogDbConnection)     
        return None


    def delete_tags_for_user(self, tags,userId , oneStopBlogDbConnection=None):
        try:             
            oneStopBlogDbConnection = createConnection()     #established connection between your database   
            result =  None   

            with oneStopBlogDbConnection.cursor() as my_cursor:   
                for tagName in tags['tags']:
                   my_cursor.callproc('SP_DelUsersTags', (tagName, userId)) 
                   oneStopBlogDbConnection.commit() 

                query = """SELECT t.tag_id, t.tag_name from UsersTags ut LEFT JOIN tags t on ut.tag_id = t.tag_id where ut.user_id = %s"""

    
                my_cursor.execute(query,( userId))

                result = my_cursor.fetchall()                                
           
            return result                
        except mysql.connector.Error as err:
            return err.msg
        except Error as e:
            return e
        finally:
            closeMysqlconnection(oneStopBlogDbConnection)     
        return None

    def get_tags_for_user(self,userId , oneStopBlogDbConnection=None):
        try:             
            oneStopBlogDbConnection = createConnection()     #established connection between your database   
            result =  None   

            with oneStopBlogDbConnection.cursor() as my_cursor:                  

                query = """SELECT t.tag_id, t.tag_name from UsersTags ut LEFT JOIN tags t on ut.tag_id = t.tag_id where ut.user_id = %s"""
   
                my_cursor.execute(query,( userId))

                result = my_cursor.fetchall()                                
           
            return result                
        except mysql.connector.Error as err:
            return err.msg
        except Error as e:
            return e
        finally:
            closeMysqlconnection(oneStopBlogDbConnection)     
        return None
    def get_all_blogs(self, oneStopBlogDbConnection=None):
        try: 
            
            oneStopBlogDbConnection = createConnection()     #established connection between your database   
            result =  None   

            with oneStopBlogDbConnection.cursor() as my_cursor:   
                
                    query = """SELECT * from Blogs"""

    
                    my_cursor.execute(query)

                    result = my_cursor.fetchall()                            
            
            return result                
        except mysql.connector.Error as err:
            return err.msg
        except Error as e:
            return e
        finally:
            closeMysqlconnection(oneStopBlogDbConnection)  

    def get_blog_by_id(self, blogId, oneStopBlogDbConnection= None):        
        try: 
            
            oneStopBlogDbConnection = createConnection()     #established connection between your database   
            result =  None   

            with oneStopBlogDbConnection.cursor() as my_cursor:   
                
                    query = """SELECT * from Blogs where Blog_id = %s LIMIT 1"""

    
                    my_cursor.execute(query, blogId)

                    result = my_cursor.fetchone()                            
            
            return result                
        except mysql.connector.Error as err:
            return err.msg
        except Error as e:
            return e
        finally:
            closeMysqlconnection(oneStopBlogDbConnection)  


    
    def delete_blog_by_id(self, blogId, oneStopBlogDbConnection= None):        
        try: 
            
            oneStopBlogDbConnection = createConnection()    #established connection between your database   
           

            with oneStopBlogDbConnection.cursor() as my_cursor:   
                
                    query = """DELETE from Blogs where Blog_id = %s"""

    
                    my_cursor.execute(query, blogId)                                           
                    oneStopBlogDbConnection.commit()  
                          
        except mysql.connector.Error as err:
            return err.msg
        except Error as e:
            return e
        finally:
            closeMysqlconnection(oneStopBlogDbConnection)    

    def get_written_blogs(self,  userId, oneStopBlogDbConnection=None):
        try:
            oneStopBlogDbConnection = createConnection()     #established connection between your database   
            result =  None           
            with oneStopBlogDbConnection.cursor() as my_cursor:                   
                            
                my_cursor.callproc('SP_GetWrittenBlogs', (userId,)) 
                oneStopBlogDbConnection.commit()               
                
                result = my_cursor.fetchall()              
            return result                
        except mysql.connector.Error as err:
            return err.msg
        except Error as e:
            return e
        finally:
            closeMysqlconnection(oneStopBlogDbConnection)                                                
# mysqlp = MySQLProvider()
# mysqlp.add_tags_for_user(["Advice"], "1")
# mysqlp.get_tag("100")
# #mysqlp.get_sql_version()   
# mysqlp.get_user_by_id_or_email("amrale.netra@gmail.com")
