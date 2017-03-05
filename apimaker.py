import boto3
import pickle
from helpers import pickle_dictionary_to_file

def create_site_retriever_api(client):
    """
    Create a new site retriever api and save its info to a file.
    """
    response = client.create_rest_api(
        name='siteretriever',
        description='get site data from a list of sites',
        version='1'
    )
    file_name = "api_info.pickle"
    pickle_dictionary_to_file(response, file_name)

def get_initial_resource(client):
    """
    Return a dictionary representing the initial parent resource.
    """
    response = client.get_resources(
        restApiId=get_api_id_from('api_info.pickle')
    )
    return response['items'][0]

def add_resource(client, api_id, parent_resource, sub_path):
    """
    Create a new resource under the parent resource,
    pickling and saving the response to a file.
    """
    response = client.create_resource(
        restApiId=api_id,
        parentId=parent_resource['id'],
        pathPart=sub_path)
    file_name = "{0}_resource.pickle".format(sub_path)
    pickle_dictionary_to_file(response, file_name)


def get_api_id_from(file):
    """
    Return the api id.
    """
    with open(file, "r") as f:
        api_info = pickle.load(f)
        return api_info['id']


if __name__ == "__main__":
    client = boto3.client('apigateway', region_name='us-east-1')
    api_id = get_api_id_from('api_info.pickle')
    initial_resource = get_initial_resource()

    add_resource(client, api_id, initial_resource, "sites")
