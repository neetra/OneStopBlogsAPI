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
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        # pass the regular expression
        # and the string into the fullmatch() method
        if(re.fullmatch(regex, email)):
            return True;
    
        else:
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
        

    def get_user_by_id_or_email(self, username):
        try: 
            isEmail = self.check(username)
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
            with oneStopBlogDbConnection.cursor() as my_cursor:                
                
                my_cursor.callproc('SP_ADDUserDetails', (user_l[JSONKeys.EMAIL],user_l[JSONKeys.FIRSTNAME], user_l[JSONKeys.LASTNAME], user_l[JSONKeys.USERTYPE])) 
                oneStopBlogDbConnection.commit()
                result = my_cursor.fetchone()
                print(result)

            return result                
        except mysql.connector.Error as err:
            return err.msg
        finally:
            closeMysqlconnection(oneStopBlogDbConnection)         
        
        return None


# mysqlp = MySQLProvider()
# #mysqlp.get_sql_version()   
# mysqlp.get_user_by_id_or_email("amrale.netra@gmail.com")
