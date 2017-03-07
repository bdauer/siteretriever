from __future__ import print_function
import boto3
import json
import io

def lambda_handler(event, context):

    lambda_client = boto3.client('lambda', region_name='us-east-1')

    for site in event['sites']:
        lambda_client.invoke(
            FunctionName='scrape_and_store',
            InvocationType='Event',
            Payload = json.dumps({'site': site, 'rank': event['sites'].index(site)}) # if this doesn't work, try io.StringIO
        )
