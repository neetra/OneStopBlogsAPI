import boto3
from config import aws_access_key_id, aws_secret_access_key
import tempfile
import os;
import shortuuid;
from werkzeug.utils import secure_filename
# from botocore.exceptions import NoCredentialsError
# import botocore;
# from datetime import datetime
# import uuid
# from mysql.connector.errors import Error
# from Files import File
# from Constants import project_tag, bucket_name
# import config
# from Helper import create_file_object


class S3Handler:
#     def __init__(self):       
#         self.session = boto3.Session( aws_access_key_id=config.aws_access_key_id, aws_secret_access_key=config.aws_secret_access_key)
#         self.s3_client = self.session.client('s3', 'us-east-2',config=botocore.config.Config(s3={'addressing_style':'path'}))
#         #self.s3_client = boto3.client('s3')
#         self.s3_resource_tag = {'Key':"resource",'Value':"s3"}
#         self.tags = [project_tag, self.s3_resource_tag]

    def __init__(self):    
        self.url = "https://one-stop-blogs.s3.us-east-2.amazonaws.com/" 
        self.s3Client = boto3.client('s3',
                            aws_access_key_id= aws_access_key_id, 
                            aws_secret_access_key= aws_secret_access_key
                            )
        self.BUCKET_NAME='one-stop-blogs'

#     def addTagsOnBucket(self, bucket_name, key, i_tags):
#         self.tags.append(i_tags)
#         self.s3_client.put_object_tagging(
#                 Bucket=bucket_name,
#                 Key=key,    
#                 Tagging={
#                 'TagSet': self.tags
#             })  
#         self.tags.clear()              

#     def delete_file(self, filename):
#         try:
#            self.s3_client.delete_object(
#             Bucket= bucket_name,
#             Key= filename)
#            return {"message" :"File not present"}           
#         except Error as e:
#             return {"message" : "Cannot delete file"}       
                     
       
    def upload_file(self, file, content_type) :
        filename = secure_filename(shortuuid.uuid() + "_"+file.filename )
        filePath = os.path.join(tempfile.gettempdir(), filename)
        file.save(filePath)

        res  = self.s3Client.upload_file(
                    Bucket = self.BUCKET_NAME,
                    Filename=filePath,
                    Key = filename,
                     ExtraArgs={'ACL':'public-read'}
                ) 
        return self.url + filename;                
        # self.s3Client.upload_fileobj(
        #     file,
        #     self.BUCKET_NAME,
        #     filename,
        #     ExtraArgs={
        #         "ACL": "public-read",
        #         "ContentType": file.content_type    #Set appropriate content type as per the file
        #     }
       # )
        # self.s3Client.put_object(Body=file,
        #               Bucket=self.BUCKET_NAME,
        #               Key=filename,
        #               ContentType=content_type)   