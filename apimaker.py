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
    with open("api_info.pickle", 'w') as f:
        pickle.dump(response, f)


def get_initial_resource():
    """
    Return a dictionary representing the initial parent resource.
    """
    client = boto3.client('apigateway', region_name='us-east-1')
    response = client.get_resources(
        restApiId=get_api_id_from('api_info.pickle')
    )
    return response['items'][0]


def add_site_retriever_resource():
    """
    """
    api_id = get_api_id_from_file('api_info.pickle')
    parent_resource = get_initial_resource()

    client = boto3.client('apigateway', region_name='us-east-1')
    response = client.create_resource(
        restApiId=api_id,
        parentId=parent_resource['id']
        pathPart='/'
    )


def get_api_id_from(file):
    with open(file, "r") as f:
        api_info = pickle.load(f)
        return api_info['id']


if __name__ == "__main__":

    get_initial_resource()
