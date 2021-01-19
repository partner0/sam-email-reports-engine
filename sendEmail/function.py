import json
import boto3
import traceback
from Common import LambdaBase

class SendEmail(LambdaBase):
    def handle(self, event, context):
        ses_client = boto3.client('ses', region_name = event['ses_region'])
        response = ses_client.send_email(
            Destination = { 'ToAddresses': event['email_to'] },
            Message = 
            {
                'Body': 
                {
                    'Text': 
                    {
                        'Charset': "UTF-8",
                        'Data': event['email_body']
                    },
                },
                'Subject': 
                {
                    'Charset': "UTF-8",
                    'Data': event['email_subject']
                },
            },
            Source = event['email_from']
        )
        return {
            "statusCode": 200,
            "ses-response": response
        }

index = SendEmail.get_handler()