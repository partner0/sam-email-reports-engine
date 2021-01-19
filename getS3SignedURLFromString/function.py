import json
import boto3
import traceback
import datetime
from Common import LambdaBase

class GetS3SignedUrlFromString(LambdaBase):
    def handle(self, event, context):
        s3 = boto3.resource("s3")
        s3_client = boto3.client("s3")
        now = datetime.datetime.now()
        s3.Bucket(event['s3_bucket']).put_object(Key = event['s3_object_name'], Body = event['s3_object_body'].encode("utf-8"))
        url = s3_client.generate_presigned_url('get_object', Params = {'Bucket': event['s3_bucket'], 'Key': event['s3_object_name']}, ExpiresIn = event['url_expire'])
        expire_datetime = now + datetime.timedelta(0, event['url_expire'])
        return {
            "statusCode": 200,
            "url": url,
            "expires-on": str(expire_datetime) + " UTC"
        }

index = GetS3SignedUrlFromString.get_handler()