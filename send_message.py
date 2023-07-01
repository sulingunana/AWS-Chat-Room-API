import json
import boto3
import os
from boto3.dynamodb.conditions import Key
import logging

def lambda_handler(event, context):
    connectionId = event['requestContext']['connectionId']
    user_name = event.get('queryStringParameters', {'name': 'guest'}).get('name')
    
    to_send = "Sulin"
    
    dynamo = boto3.resource('dynamodb').Table(os.environ['TABLE_NAME'])
    resultU = dynamo.scan(FilterExpression=Key('user_name').eq(to_send))
    
    receiver_id = resultU['Items'][0]['connectionId']
    
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logger.info(receiver_id)
    

    domain = event["requestContext"]["domainName"]
    stage = event["requestContext"]["stage"]
    apig_management_client = boto3.client('apigatewaymanagementapi', endpoint_url=f'https://{domain}/{stage}')
        

    logger.info("Trying to send")

    apig_management_client.post_to_connection(Data="test", ConnectionId=receiver_id)
    logger.info("sended")
    
    return {"statusCode": 201}