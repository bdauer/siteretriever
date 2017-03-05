import boto3
import json
from datetime import datetime
import pickle


def create_site_retriever_api():
    """
    Create a new site retriever api and save its info to a file.
    """
    client = boto3.client('apigateway', region_name='us-east-1')
    response = client.create_rest_api(
        name='siteretriever',
        description='get site data from a list of sites',
        version='1'
    )
    with open("api_info.json", 'w') as f:
        pickle.dump(response, f)


if __name__ == "__main__":

    create_site_retriever_api()
