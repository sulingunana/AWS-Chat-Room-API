import json
import boto3
import os
import logging

def lambda_handler(event, context):
    connectionId = event['requestContext']['connectionId']
    user_name = event.get('queryStringParameters', {'name': 'guest'}).get('name')

    table = boto3.resource('dynamodb').Table(os.environ['TABLE_NAME'])
    
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    kime = event.get('body', {}).get('kime')
    
    scan_response = table.scan(ProjectionExpression='connectionId')
    connection_ids = [item['connectionId'] for item in scan_response['Items']]
    logger.info("Found %s active connections.", len(connection_ids))
    
    domain = event.get('requestContext', {}).get('domainName')
    stage = event.get('requestContext', {}).get('stage')

    apig_management_client = boto3.client('apigatewaymanagementapi', endpoint_url=f'https://{domain}/{stage}')
    
    logger.info("sending message to message owner")
    apig_management_client.post_to_connection(Data="test", ConnectionId=connectionId)
    
    for other_conn_id in connection_ids:
        logger.info("Sendind a message to id: %s", other_conn_id)
        send_response = apig_management_client.post_to_connection(Data="SELAMM", ConnectionId=other_conn_id)

    """
    if not user:
        return {
            'statusCode': 400,
            'body': 'User not found'
        }
    """

    #receiver_connection_id = user['Item']['connection_id']
    
    #receiver_connection_id = connection_ids.get(kime)

    send_response = apig_management_client.post_to_connection(Data="selam test!", ConnectionId=receiver_connection_id)

