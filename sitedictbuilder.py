from __future__ import print_function
import boto3
# import requests



def lambda_handler(event, context):

    for site in event['sites']:
        print(site)
