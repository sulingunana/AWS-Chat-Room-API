import json
import boto3
import os

def lambda_handler(event, context):
    connectionId = event['requestContext']['connectionId']
    userId = event.get('queryStringParameters', {}).get('name')

    dynamo = boto3.resource('dynamodb').Table(os.environ['TABLE_NAME'])

    dynamo.delete_item(Key={'connectionId': connectionId})
