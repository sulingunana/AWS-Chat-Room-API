import json
import boto3
import os
from boto3.dynamodb.conditions import Key
import logging

def lambda_handler(event, context):
    connectionId = event['requestContext']['connectionId']

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    
    logger.info(f"event: {event}")
    
    to_send = json.loads(event['body']).get('to', None)
    user_name = json.loads(event['body']).get('from', None)
    message = json.loads(event['body']).get('message', None)
    
    domain = event["requestContext"]["domainName"]
    stage = event["requestContext"]["stage"]
    
    apig_management_client = boto3.client('apigatewaymanagementapi', endpoint_url=f'https://{domain}/{stage}')

    if not message:
        json_data = {"status": "failed", "message": "not_delivered", "data": "Missing parameter 'message'"}
        apig_management_client.post_to_connection(Data=json.dumps(json_data), ConnectionId=connectionId)
        return {"statusCode": 404}
    
    if not to_send:
        json_data = {"status": "failed", "message": "not_delivered", "data": "Missing parameter 'to'"}
        apig_management_client.post_to_connection(Data=json.dumps(json_data), ConnectionId=connectionId)
        return {"statusCode": 404}

    if not user_name:
        json_data = {"status": "failed", "message": "not_delivered", "data": "Missing parameter 'from'"}
        apig_management_client.post_to_connection(Data=json.dumps(json_data), ConnectionId=connectionId)
        return {"statusCode": 404}

    dynamo = boto3.resource('dynamodb').Table(os.environ['TABLE_NAME'])
    
    logger.info(f"Searching user on db")
    resultU = dynamo.scan(FilterExpression=Key('user_name').eq(to_send))
    logger.info(f"resultU: {resultU}")
    if resultU["Count"] == 0:
        # user is not online or not found
        logger.info(f"User not found on db")
        json_data = {"status": "failed", "message": "not_delivered", "data": "User not found or not online"}
        apig_management_client.post_to_connection(Data=json.dumps(json_data), ConnectionId=connectionId)
        return {"statusCode": 404}

    # json_data = {"Message":{"from":user_name,"data":message}}
    json_data = {"status": "success", "message": "received", "data": {"from": user_name, "to": to_send, "msg": message}}
    receiver_id = resultU['Items'][0]['connectionId']

    logger.info(f"json_data: {json_data}")

    apig_management_client.post_to_connection(Data=json.dumps(json_data), ConnectionId=receiver_id)
    
    return {"statusCode": 200}