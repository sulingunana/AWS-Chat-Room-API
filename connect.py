import json
import boto3
import os

def lambda_handler(event, context):
    connectionId = event['requestContext']['connectionId']
    user_name = event.get('queryStringParameters', {'name': 'guest'}).get('name')

    dynamo = boto3.resource('dynamodb').Table(os.environ['TABLE_NAME'])
    
    json_data = {
        'user_name': user_name,
        'connectionId': connectionId
    }


    dynamo.put_item(Item=json_data)
    
    return {
        'statusCode': 200,
        'headers': {"status": "success"},
        'body': 'Welcome to the chat api!'
    }