import boto3
import os


s3_client = boto3.client('s3')


def lambda_handler(event, context):
    print('YAY!')
    # s3_client.upload_file(upload_path, '{}-resized'.format(bucket), key)