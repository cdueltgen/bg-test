import os

import boto3

S3_BUCKET = os.environ.get('S3_BUCKET')


def upload_queue(filename, file_contents):
    """Upload to s3 function for use with the worker queue."""
    # file_contents = f.read()

    s3 = boto3.resource('s3')
    s3.Bucket(S3_BUCKET).put_object(Key=filename, Body=file_contents)
    return
