from configparser import Error


from logging import error
from flask import Flask, request, current_app, jsonify
from flask_jwt import JWT, jwt_required
from pymysql import IntegrityError

from MySQLProvider import MySQLProvider
from datetime import datetime
from secrets import token_urlsafe;

import os, sys;
from flask_cors import CORS
import os, tempfile, zipfile
from Models.User import User
from S3Handler import S3Handler

# Initialize mysql and s3 handlers
mysqlprovider = MySQLProvider()


# User Object for JWT authentication
# class User(object):
#     def __init__(self, user_id, email, first_name, last_name, role_id =2):
#         self.user_id = user_id
#         self.email = email
#         self.first_name = first_name
#         self.last_name = last_name
#         self.role_id = role_id
#     def __str__(self):
#         return "User(id='%s')" % self.id


# Customize payload operation to encode role of the user.
def make_payload(identity):  
    iat = datetime.utcnow()
    exp = iat + current_app.config.get('JWT_EXPIRATION_DELTA')
    nbf = iat + current_app.config.get('JWT_NOT_BEFORE_DELTA')
    return {
        'exp': exp, 'iat': iat, 'nbf': nbf,
        'userId': identity.userId,
        'userType' : identity.type,
        'firstName' : identity.firstName,
        'lastName': identity.lastName,
        'email': identity.email,
        'service':'OneStopBlogs'
        }  

def authenticate(username, password):
   
    # Get userdetails from mysql
    user = mysqlprovider.get_user_by_id_or_email(username)
    if(user is None):
        return "Unauthorized user"            

    userObj = User()
    userObj.email = user["Email"]
    userObj.firstName = user["firstName"]
    userObj.lastName = user["lastName"]
    userObj.type = user["typeId"]
    userObj.userId = user["userId"]    
    return userObj

# This is called when jwt-required
def identity(payload):
    user_id = payload['userId']
    user = mysqlprovider.get_user_by_id_or_email(user_id)

    
    if (user is None):
        return None  

    userObj = User()
    userObj.email = user["Email"]
    userObj.firstName = user["firstName"]
    userObj.lastName = user["lastName"]
    userObj.type = user["typeId"]
    userObj.userId = user["userId"]    
    return userObj;
          

# Initialise Flask APP
app = Flask(__name__)
app.config['SECRET_KEY'] = token_urlsafe(16)  

# Enable CORS to all origins 
cors = CORS(app)

# JWT initialization
jwt = JWT(app, authenticate, identity)
jwt.jwt_payload_callback = make_payload

# # Sign up new user 
# @app.route('/create-user',  methods = ["POST"])
# def create_user():
#      print("create a user")
#      json_data = request.get_json()  
#      print(json_data)     
#      user  = mysqlprovider.create_user(json_data)
     
#      if user is None:
#          return "Bad request either username exist or password not valid",400
#      else:
#          return "User is created", 200

def get_role_id(token):     
    decoded_token = decode_token(token)
    role_id =  decoded_token['role_id']
    return role_id

def get_email(token):     
    decoded_token = decode_token(token)
    return decoded_token['email']    

def decode_token(token)   :      
    try:          
        token = token.split(" ")[1]
        decode = jwt.jwt_decode_callback(token)
        return decode;
    except error as e:
        return e        
    
def getTokenFromAuthorizationHeader():
    try:
        token = request.headers["Authorization"]        
        return token
    except:
        return "Error while parsing token"        

# # create, edit new file , upload functionality
# @app.route("/createfile", methods = ["POST"])
# @jwt_required()
# def create_a_file():  
#     try:   
#         # Lambda function has read-only access only temp directory     
#         with tempfile.TemporaryDirectory() as tmpdir:
#             print(tmpdir)
#         token = request.headers["Authorization"]
#         email = get_email(token) ;        
#         f = request.files['file_key']        
#         tmpdir = os.path.dirname(tmpdir)
#         dirname = os.path.join(tmpdir, f.filename)      
#         f.save(dirname);        
#         file  = s3_handler.upload_file(dirname,email)          
#         os.remove(dirname)         
#         mysqlprovider.add_entry_of_file(file, email)        
#         return "Success", 200
#     except Error as err:
#         return {"message":err.message},400       

@app.route("/user/<username>")
def get_user_details_by_userId_or_email(username):
    try:
        result = mysqlprovider.get_user_by_id_or_email(username)
        return result
    except Error as e:
        return {"message" : e.message}        , 400



@app.route("/user", methods =["POST"])
def create_new_user():
    try:
        content = request.json
        result = mysqlprovider.create_user(content)
        return result
    except IntegrityError as e:
        return {"message" : e.args[1]}, 409        
    except Error as e:
        print(e.message)
        return {"message" : e.message}, 409        

@app.route("/pingToken")
@jwt_required()
def ping_validity_of_token():
    try:        
        return {"message" : "Success"}, 200
    except Error as e:
        return "Error " + e, 400

@app.route("/ping")
def ping():
    try:           
        return {'message' : 'success'}, 200
    except Error as e:
        return "Error " + e, 400


@app.route("/pingRDS")
def ping_RDS():
    try: 
        result  = mysqlprovider.get_sql_version()
        if result is not None:          
            return {'message' : 'success'}, 200
        else :
            return  {'message' : 'Cannot connect RDS'}, 500         
    except Error as e:
        return "Error " + e, 400        

@app.route("/")
def home():
    try:           
        return {'message' : 'success'}, 200
    except Error as e:
        return "Error " + e, 400  


@app.route("/tags")
def get_tags()              :
    try:
       
        result = mysqlprovider.get_tags()
        return jsonify(result)
    except IntegrityError as e:
        return {"message" : e.args[1]}, 409        
    except Error as e:
        print(e.message)
        return {"message" : e.message}, 409   
 
@app.route("/tag", methods = ["GET"])
def get_tag()              :
    try:
        if request.method == "GET":
            param= request.args['name']

            result = mysqlprovider.get_tag(param)
            return jsonify(result)
    except IntegrityError as e:
        return {"message" : e.args[1]}, 409        
    except Error as e:
        print(e.message)
        return {"message" : e.message}, 409   

 
@app.route("/uploadImage", methods = ["POST"])
def upload_image()              :
    try:
        if request.method == "POST":
            f = request.files['file']
            s3handler = S3Handler();
            url = s3handler.upload_file(f, f.mimetype)
            #result = mysqlprovider.get_tag(param)
            return jsonify({"imageLink": url})
    except IntegrityError as e:
        return {"message" : e.args[1]}, 409        
    except Error as e:
        print(e.message)
        return {"message" : e.message}, 409   

@app.route("/blog", methods = ["POST", "GET", "DELETE"])
def operations_blog()              :
    try:
        if request.method == "POST":
            jsonData = request.json
            param= request.args.get('userId')
            result = mysqlprovider.add_blog(jsonData, param)
            return jsonify(result)
        elif request.method == "GET":
            param= request.args['blogId']            
            result = mysqlprovider.get_blog_by_id(param)
            return jsonify(result)
        elif request.method == "DELETE":
            param= request.args['blogId']            
            mysqlprovider.delete_blog_by_id(param)
            msg = "Successfully deleted the blog with id : " + param 
            return jsonify({"message" :msg})            
    except IntegrityError as e:
        return {"message" : e.args[1]}, 409        
    except Error as e:
        print(e.message)
        return {"message" : e.message}, 409   

@app.route("/blogs", methods = ["GET"])
def get_all_blogs()              :
    try:
        if request.method == "GET":  
            userId = request.args.get('userId')
            if userId is not None:
                result = mysqlprovider.get_written_blogs(userId=userId)      
            else:
              result = mysqlprovider.get_all_blogs()
            return jsonify(result)
    except IntegrityError as e:
        return {"message" : e.args[1]}, 409        
    except Error as e:
        print(e.message)
        return {"message" : e.message}, 409   

@app.route("/usertags", methods = ["POST", "DELETE", "GET"])
def user_tags()              :
    try:
        if request.method == "POST":
            param= request.args['userId']
            tags = request.json
            result = mysqlprovider.add_tags_for_user( tags, param)
            return jsonify({param : result})
        if request.method == "DELETE":
            param= request.args['userId']
            tags = request.json
            result = mysqlprovider.delete_tags_for_user( tags, param)
            return jsonify({param : result})
        if request.method == "GET":
            param= request.args['userId']            
            result = mysqlprovider.get_tags_for_user( param)
            return jsonify({param : result})
    except IntegrityError as e:
        return {"message" : e.args[1]}, 409        
    except Error as e:
        print(e.message)
        return {"message" : e.message}, 409   
        
if __name__ == '__main__':
    app.run()