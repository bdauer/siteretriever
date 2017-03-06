from __future__ import print_function
import boto3
import json
import io
from tablebuilder import create_table

def lambda_handler(event, context):
    '''
    create a siteDict table.
    use one of the values as the primarykey for each item. e.g. rank.
    '''
    # table is created here so that it's only created once.
    table_name = 'siteDict'
    attribute_list = [('name', 'S', 'HASH'), ('rank', 'N', 'RANGE')]
    create_table(table_name, attribute_list)

    lambda_client = boto3.client('lambda', region_name='us-east-1')

    for site in event['sites']:
        lambda_client.invoke(
            FunctionName='scrape_and_store',
            InvocationType='Event'
            Payload = json.dumps({'site': site, 'rank': event['sites'].index(site)}) # if this doesn't work, try io.StringIO
        )
