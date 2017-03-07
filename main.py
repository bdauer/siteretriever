import boto3
from tablebuilder import create_table
from lambdabuilder import add_function
from apimaker import setup_method_with_lambda, get_resource, get_api_id_from
if __name__ == '__main__':


    # db_client = boto3.client('dynamodb', region_name='us-east-1')
    # table_name = 'siteDict'
    # attribute_list = [('name', 'S', 'HASH'), ('rank', 'N', 'RANGE')]
    # create_table(db_client, table_name, attribute_list)

    ## add the lambdas
    client = boto3.client('lambda', region_name='us-east-1')
    iam = boto3.resource('iam')
    # need to eventually create more specific roles.
    role = iam.Role('lambda-dynamodb-execution-role')

    # add_function(client, 'dictionary_builder', 'python2.7', role,
    #              'sitedictbuilder.lambda_handler',
    #              'sitedictbuilder.zip')

    add_function(client, 'scrape_and_store', 'python2.7', role,
                 'awssiteretriever.lambda_handler',
                 'awssiteretriever.zip')


    # add the method to the resource
    # api_client = boto3.client('apigateway', region_name='us-east-1')
    # api_id = get_api_id_from('api_info.pickle')
    # resource = get_resource(api_client, api_id, 'sites')
    # setup_method_with_lambda(api_client, api_id, resource, 'POST', 'None', 'AWS',
    #                          'us-east-1', 'dictionary_builder')
