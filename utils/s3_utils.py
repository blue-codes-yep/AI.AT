import boto3
import os
from botocore.exceptions import NoCredentialsError
from apikey import aws_access_key, aws_secret_key
from .progress_utils import celery
# AWS S3 credentials
AWS_ACCESS_KEY_ID = aws_access_key
AWS_SECRET_ACCESS_KEY = aws_secret_key
BUCKET_NAME = 'videos.yt'

s3 = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
@celery.task(bind=True)
def upload_to_s3(file_path, object_name):
    try:
        s3.upload_file(
            file_path,
            BUCKET_NAME,
            os.path.basename(object_name),
            ExtraArgs={
                'ContentType': 'video/mp4'
            }
        )
        print(object_name, "uploaded to S3")
        url = f"https://s3.amazonaws.com/{BUCKET_NAME}/{object_name.split('/')[-1]}"
        print("URL:", url)
        return url
    except FileNotFoundError:
        print("File not found")
        return None
    except NoCredentialsError:
        print("Credentials not available")
        return None
