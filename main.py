import boto3
import json
from tablebuilder import create_table
from lambdabuilder import add_function
from apimaker import (setup_method_with_lambda, get_resource,
                      get_api_id_from, get_initial_resource, add_resource,
                      create_site_retriever_api)

if __name__ == '__main__':
    print("adding role...")
    access_client = boto3.client('iam', region_name='us-east-1')
    iam = boto3.resource('iam')

    assume_role_policy_document = json.dumps(
        {"Version":"2012-10-17",
         "Statement":
            [{"Effect": "Allow",
              "Action": "sts:AssumeRole",
              "Principal": {
                "Service": "lambda.amazonaws.com"
                 }
            }]
        }
    )
    access_client.create_role(
        RoleName='site-retrieval-role',
        AssumeRolePolicyDocument=assume_role_policy_document)

    # unsafe and redundant. would need to pin this down better for actual use.
    arns = ['arn:aws:iam::aws:policy/AmazonDynamoDBFullAccess',
            'arn:aws:iam::aws:policy/AWSLambdaFullAccess']

    for arn in arns:
        access_client.attach_role_policy(
            RoleName='site-retrieval-role',
            PolicyArn=arn
        )
    role = iam.Role('site-retrieval-role')

    print("building dyamodb table..")
    db_client = boto3.client('dynamodb', region_name='us-east-1')
    table_name = 'siteDict'
    attribute_list = [('name', 'S', 'HASH'), ('rank', 'N', 'RANGE')]
    create_table(db_client, table_name, attribute_list)

    print("adding lambda functions...")
    lambda_client = boto3.client('lambda', region_name='us-east-1')
    iam = boto3.resource('iam')

    add_function(lambda_client, 'dictionary_builder', 'python2.7', role,
                 'sitedictbuilder.lambda_handler',
                 'sitedictbuilder.zip')

    add_function(lambda_client, 'scrape_and_store', 'python2.7', role,
                 'awssiteretriever.lambda_handler',
                 'awssiteretriever.zip')

    add_function(lambda_client, 'site_data_retriever', 'python2.7', role,
                 'sitedataretriever.lambda_handler',
                 'sitedataretriever.zip')

    print("building api...")
    api_client = boto3.client('apigateway', region_name='us-east-1')
    create_site_retriever_api(api_client)
    api_id = get_api_id_from('api_info.pickle')

    print("adding resources...")
    initial_resource = get_initial_resource(api_client, api_id)
    resources = ['sitedata', 'sites']
    for resource in resources:
        add_resource(api_client, api_id, initial_resource, resource)
    GET_resource = get_resource(api_client, api_id, 'sitedata')
    POST_resource = get_resource(api_client, api_id, 'sites')

    # add the POST method to the resource
    print("linking lambdas to api endpoints...")
    setup_method_with_lambda(api_client, api_id, POST_resource, 'POST', 'None',
                                'AWS','us-east-1', 'dictionary_builder')

    # add the GET method to the resource
    setup_method_with_lambda(api_client, api_id, GET_resource, 'GET', 'None',
                             'AWS', 'us-east-1', 'site_data_retriever')
    print("setup complete!")
