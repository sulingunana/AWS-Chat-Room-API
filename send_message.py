import json
import boto3
import os
from boto3.dynamodb.conditions import Key
import logging

def lambda_handler(event, context):
    connectionId = event['requestContext']['connectionId']
    user_name = event.get('queryStringParameters', {'name': 'guest'}).get('name')
    
    to_send = json.loads(event['body']).get('to_send', None)
    message = json.loads(event['body']).get('message', None)

    if not message:
        return {"statusCode": 400, "body": "Missing parameter 'message'"}
    
    if not to_send:
        return {"statusCode": 400, "body": "Missing parameter 'to_send'"}

    dynamo = boto3.resource('dynamodb').Table(os.environ['TABLE_NAME'])
    resultU = dynamo.scan(FilterExpression=Key('user_name').eq(to_send))

    result_count = resultU['Count']
    scaned_colunt = resultU['ScannedCount']

    json_data = {"Message":{"from":user_name,"data":message},"result_count": result_count, "scaned_colunt": scaned_colunt}
    
    receiver_id = resultU['Items'][0]['connectionId']
    
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logger.info(receiver_id)
    

    domain = event["requestContext"]["domainName"]
    stage = event["requestContext"]["stage"]
    apig_management_client = boto3.client('apigatewaymanagementapi', endpoint_url=f'https://{domain}/{stage}')

    logger.info("Trying to send")
    logger.info(json_data)

    apig_management_client.post_to_connection(Data=json.dumps(json_data), ConnectionId=receiver_id)
    logger.info("sended")
    
    return {"statusCode": 201, "body": "sended"}