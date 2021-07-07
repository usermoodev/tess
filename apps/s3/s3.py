import boto3
s3 = boto3.client('s3', endpoint_url='https://s3gw.inet.co.th:8082',
                  aws_access_key_id='OQINHJTDIYDKDZNC7BQV',
                  aws_secret_access_key='6JAnvBYVFTY/rvQa7LmljpD2rM79jZl9k9FdnZub', verify=False )

bucket_name = "ocrproject"
path_s3 = "wood_detection/"

def s3_upload(path_file,path_s3,filename):
    s3.upload_file(path_file, bucket_name, path_s3 + filename)


def s3_generatelink(s3_path, filename):
    file_path = s3_path + filename
    link = s3.generate_presigned_url('get_object', Params={'Bucket': bucket_name, 'Key': file_path},ExpiresIn=6.30e+7)
    return link
