from configparser import Error
from tabnanny import check
from typing import Tuple
import mysql.connector 
from Files import File
from MySQLHelper import closeMysqlconnection, createConnection
from datetime import datetime
import config
from Helper import get_time_from_string;
from werkzeug.security import generate_password_hash, check_password_hash
from mysql.connector.cursor import MySQLCursorDict, MySQLCursorPrepared
import re
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
 

    def get_sql_version(self):
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
            closeMysqlconnection(oneStopBlogDbConnection, my_cursor)                   
        
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
            closeMysqlconnection(oneStopBlogDbConnection, my_cursor)         
        
        return None

    def create_user(self, user_l):
        try:      
            
            oneStopBlogDbConnection =mysql.connector.connect(host=config.db_host,user=config.db_username,password=config.db_password,database=config.db_database)#established connection between your database   
            
            my_cursor=oneStopBlogDbConnection.cursor()    
            hash_password = generate_password_hash(user_l["password"])    
            my_cursor.callproc('SP_AddNewUser', (user_l['email'],  user_l['first_name'], user_l['last_name'], hash_password))       
            oneStopBlogDbConnection.commit()
            results = my_cursor.stored_results()
            for result in results:
                return result.fetchone()
        except mysql.connector.Error as err:
            print (err)          
            
        finally:
            closeMysqlconnection(oneStopBlogDbConnection, my_cursor)  
        return None    


mysqlp = MySQLProvider()
#mysqlp.get_sql_version()   
mysqlp.get_user_by_id_or_email("amrale.netra@gmail.com")
