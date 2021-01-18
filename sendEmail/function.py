import json
import boto3
import traceback

def index(event, context):
    try:
        for variable in event:
            globals()[variable] = event[variable]
        ses_client = boto3.client('ses', region_name = ses_region)
        response = ses_client.send_email(
            Destination = { 'ToAddresses': email_to },
            Message = 
            {
                'Body': 
                {
                    'Text': 
                    {
                        'Charset': "UTF-8",
                        'Data': email_body
                    },
                },
                'Subject': 
                {
                    'Charset': "UTF-8",
                    'Data': email_subject
                },
            },
            Source = email_from
        )
    except:
        return {
            "statusCode": 500,
            "message": traceback.format_exc(),
        }
    return {
        "statusCode": 200,
        "ses-response": response
    }