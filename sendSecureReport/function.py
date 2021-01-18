import json
import boto3
import os
import traceback
import datetime

def index(event, context):
    try:
        for variable in event:
            globals()[variable] = event[variable]
        lambda_client = boto3.client("lambda")
        params = {
            "db_host": db_host,
            "db_port": db_port,
            "db_name": db_name,
            "db_user_ro": db_user_ro,
            "db_pass": db_pass,
            "sql_query": sql_query
        }
        response = lambda_client.invoke(
            FunctionName = os.environ['getCsvDataFromPsql'],
            InvocationType = "RequestResponse",
            Payload = json.dumps(params)
        )
        csv = json.load(response['Payload'])['csv']
        params = {
            "s3_object_body": csv,
            "s3_bucket": s3_bucket,
            "url_expire": url_expire
        }
        response = lambda_client.invoke(
            FunctionName = os.environ['getS3SignedURLFromString'],
            InvocationType = "RequestResponse",
            Payload = json.dumps(params)
        )
        response = json.load(response['Payload'])
        url = response['url']
        params = {
            "email_from": email_from,
            "email_to": email_to,
            "email_subject": email_subject,
            "email_body": email_body.format(url, response['expires-on']),
            "ses_region": ses_region
        }
        response = lambda_client.invoke(
            FunctionName = os.environ['sendEmail'],
            InvocationType = "RequestResponse",
            Payload = json.dumps(params)
        )
    except:
        return {
            "statusCode": 500,
            "message": traceback.format_exc().split("\n"),
        }
    return {
        "satusCode": 200,
        "report-url": url,
        "ses-response": json.load(response['Payload'])['ses-response']
    }