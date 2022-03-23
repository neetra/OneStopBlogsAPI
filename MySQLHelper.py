import config
import mysql.connector 
import pymysql.cursors
def createConnection():
        onestopblog_db=pymysql.connect(host=config.db_host,user=config.db_username,password=config.db_password,database=config.db_database,
         cursorclass=pymysql.cursors.DictCursor
        )#established connection between your database  
        return onestopblog_db   

def closeMysqlconnection(mysql_db : pymysql, my_cursor):
    if mysql_db:
            mysql_db.close()            
            
            print("MySQL connection is closed")

