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


def add_integration(client, api_id, resource, http_method, i_type):
    """
    Link a lambda function to an API gateway.
    """
    with open("dictionary_builder_lambda.pickle") as f:
        function_arn = pickle.load(f)['FunctionArn']
    region = 'us-east-1'
    uri =\
"arn:aws:apigateway:{0}:lambda:path/2015-03-31/functions/{1}/invocations".format(
                                                    region, function_arn)
    response = client.put_integration(
        restApiId=api_id,
        resourceId=resource['id'],
        httpMethod=http_method,
        type=i_type,
        integrationHttpMethod=http_method,
        uri=uri)
    print(response)

def add_method(client, api_id, resource, http_method, authorization_type):
    """
    Add a method to an API gateway.
    """
    response = client.put_method(
        restApiId=api_id,
        resourceId=resource['id'],
        httpMethod=http_method,
        authorizationType=authorization_type
        )

def get_api_id_from(file):
    """
    Return the api id.
    """
    with open(file, "r") as f:
        api_info = pickle.load(f)
        return api_info['id']


def get_resource(client, api_id, path_part):
    """
    Return a resource dictionary.
    The path_part is used to identify the dictionary.
    """
    response = client.get_resources(
        restApiId=api_id
    )
    for item in response['items']:
        try:
            if item['pathPart'] == path_part:
                resource = item
        except KeyError:
            continue
    return resource

def get_initial_resource(client, api_id):
    """
    Return a dictionary representing the initial parent resource.
    """
    response = client.get_resources(
        restApiId=api_id
    )
    return response['items'][0]


if __name__ == "__main__":
    client = boto3.client('apigateway', region_name='us-east-1')
    api_id = get_api_id_from('api_info.pickle')
    resource = get_resource(client, api_id, 'sites')
    add_integration(client, api_id, resource, 'POST', 'AWS')
