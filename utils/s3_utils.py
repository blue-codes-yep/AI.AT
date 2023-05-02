import boto3
import os
from botocore.exceptions import NoCredentialsError
from apikey import aws_access_key, aws_secret_key
# AWS S3 credentials
AWS_ACCESS_KEY_ID = aws_access_key
AWS_SECRET_ACCESS_KEY = aws_secret_key
BUCKET_NAME = 'videos.yt'

s3 = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

def upload_to_s3(file_path, object_name):
    try:
        s3.upload_file(file_path, BUCKET_NAME, os.path.basename(object_name))
        url = f"https://{BUCKET_NAME}.s3.amazonaws.com/{object_name}"
        print("URL:", url)
        return url
    except FileNotFoundError:
        print("File not found")
        return None
    except NoCredentialsError:
        print("Credentials not available")
        return None
