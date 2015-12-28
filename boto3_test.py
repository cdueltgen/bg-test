import os
import boto3

from make_report import make_pdf

small_img = '/tmp/IMG_0807.JPG'
large_img = '/tmp/DSC00006.JPG'

s3_bucket = os.environ.get('S3_BUCKET')
# print s3_bucket, type(s3_bucket)

s3 = boto3.resource('s3')

# Testing to see if credentials in config work
# for bucket in s3.buckets.all():
#     print bucket.name

# data = open(small_img, 'rb')
# s3.Bucket(s3_bucket).put_object(Key='test.jpg', Body=data)

# data = open(large_img, 'rb')
# s3.Bucket(s3_bucket).put_object(Key='test-big.jpg', Body=data)

# objects = s3.Bucket(s3_bucket).objects.all()

# print objects

# for obj in objects:
#     print obj.last_modified

report = make_pdf()
data = open(report, 'rb')
s3.Bucket(s3_bucket).put_object(Key=report, Body=data)
