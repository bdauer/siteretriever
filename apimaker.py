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

def setup_method_with_lambda(client, api_id, resource, http_method,
                             authorization_type, integration_type,
                             region, function_name):
    """
    Add a lambda method to the provided resource and deploy it.
    """
    # add an http method to the resource.
    client.put_method(
        restApiId=api_id,
        resourceId=resource['id'],
        httpMethod=http_method,
        authorizationType=authorization_type
    )
    with open("{0}_lambda.pickle".format(function_name)) as f:
        function_arn = pickle.load(f)['FunctionArn']
    region = 'us-east-1'
    uri =\
"arn:aws:apigateway:{0}:lambda:path/2015-03-31/functions/{1}/invocations".format(
                                                    region, function_arn, function_name)
    # add an integration to the resource
    client.put_integration(
        restApiId=api_id,
        resourceId=resource['id'],
        httpMethod=http_method,
        type=integration_type,
        integrationHttpMethod='POST',
        uri=uri)

    client.put_method_response(
        restApiId=api_id,
        resourceId=resource['id'],
        httpMethod=http_method,
        statusCode='200'
        )

    client.put_integration_response(
        restApiId=api_id,
        resourceId=resource['id'],
        httpMethod=http_method,
        statusCode="200",
        # need empty selection pattern due to bug. See bug here:
        # https://github.com/aws/aws-sdk-ruby/issues/1080
        selectionPattern=''
        )

    client.create_deployment(
        restApiId=api_id,
        stageName="prod"
        )

    lambda_client = boto3.client('lambda', region_name='us-east-1')
    lambda_client.add_permission(
        FunctionName=function_name,
        StatementId="apigateway-siteretriever",
        Action="lambda:InvokeFunction",
        Principal="apigateway.amazonaws.com"
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
    setup_method_with_lambda(client, api_id, resource, 'POST', 'None', 'AWS',
                             'us-east-1', 'dictionary_builder')
