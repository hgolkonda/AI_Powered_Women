import boto3

def upload_to_s3(file_path, bucket, s3_key):
    s3 = boto3.client('s3')
    s3.upload_file(file_path, bucket, s3_key)
    print(f"Uploaded to s3://{bucket}/{s3_key}")
