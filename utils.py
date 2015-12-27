import boto3
import os

S3_BUCKET = os.environ.get('S3_BUCKET')


def upload_queue(filename, file_contents):
    s3 = boto3.resource('s3')
    s3.Bucket(S3_BUCKET).put_object(Key=filename, Body=file_contents)
    return
