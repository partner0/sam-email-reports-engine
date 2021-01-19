import json
import boto3
import os
import traceback
import datetime
from Common import LambdaBase

class SendSecureReport(LambdaBase):
    def handle(self, event, context):
        lambda_client = boto3.client("lambda")
        params = {
            "db_host": event['db_host'],
            "db_port": event['db_port'],
            "db_name": event['db_name'],
            "db_user_ro": event['db_user_ro'],
            "db_pass": event['db_pass'],
            "sql_query": event['sql_query']
        }
        response = lambda_client.invoke(
            FunctionName = os.environ['getCsvDataFromPsql'],
            InvocationType = "RequestResponse",
            Payload = json.dumps(params)
        )
        csv = json.load(response['Payload'])['csv']
        params = {
            "s3_object_name": event['s3_object_name'],
            "s3_object_body": csv,
            "s3_bucket": event['s3_bucket'],
            "url_expire": event['url_expire']
        }
        response = lambda_client.invoke(
            FunctionName = os.environ['getS3SignedURLFromString'],
            InvocationType = "RequestResponse",
            Payload = json.dumps(params)
        )
        response = json.load(response['Payload'])
        url = response['url']
        params = {
            "email_from": event['email_from'],
            "email_to": event['email_to'],
            "email_subject": event['email_subject'],
            "email_body": event['email_body'].format(url, response['expires-on']),
            "ses_region": event['ses_region']
        }
        response = lambda_client.invoke(
            FunctionName = os.environ['sendEmail'],
            InvocationType = "RequestResponse",
            Payload = json.dumps(params)
        )
        return {
            "satusCode": 200,
            "report-url": url,
            "ses-response": json.load(response['Payload'])
        }

index = SendSecureReport.get_handler()