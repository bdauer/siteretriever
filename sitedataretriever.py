from __future__ import print_function
import boto3

def lambda_handler(event, context):
    db_client = boto3.client('dynamodb', region_name='us-east-1')

    response = db_client.scan(
        TableName="siteDict")
    print(response["Items"])
    return response["Items"]
