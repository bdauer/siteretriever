import boto3
import pickle
import os
from helpers import pickle_dictionary_to_file

def add_function(client, function_name, runtime, role, handler, code):
    """
    Make a new lambda function.
    """
    response = client.create_function(
        FunctionName=function_name,
        Runtime=runtime,
        Role=role.arn,
        Handler=handler,
        Code={'ZipFile': open(code, 'rb').read()}
        )
    file_name = "{0}_lambda.pickle".format(function_name)
    pickle_dictionary_to_file(response, file_name)


if __name__ == "__main__":
    client = boto3.client('lambda', region_name='us-east-1')
    iam = boto3.resource('iam')
    role = iam.Role('lambda-dynamodb-execution-role')

    add_function(client, 'dictionary_builder', 'python2.7',
                 role,
                 'sitedictbuilder.lambda_handler',
                 'sitedictbuilder.zip')
