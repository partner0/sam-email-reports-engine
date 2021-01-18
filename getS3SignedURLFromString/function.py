import json
import boto3
import traceback
import datetime

def index(event, context):
    try:
        for variable in event:
            globals()[variable] = event[variable]
        s3 = boto3.resource("s3")
        s3_client = boto3.client("s3")
        now = datetime.datetime.now()
        object_name =  str(now) + ".csv"
        s3.Bucket(s3_bucket).put_object(Key = object_name, Body = s3_object_body.encode("utf-8"))
        url = s3_client.generate_presigned_url('get_object', Params = {'Bucket': s3_bucket, 'Key': object_name}, ExpiresIn = url_expire)
        expire_datetime = now + datetime.timedelta(0,url_expire)
    except:
        return {
            "statusCode": 500,
            "message": traceback.format_exc(),
        }
    return {
        "statusCode": 200,
        "url": url,
        "expires-on": str(expire_datetime) + " UTC"
    }