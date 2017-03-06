from __future__ import print_function
import boto3


def create_table(table_name, attribute_list, read_capacity=4, write_capacity=4):
    """
    Build a table, using the attribute_list of tuples to create the attributes.

    attribute_list format: [('name', 'type', 'keytype')]
    """
    attribute_definitions = []
    key_schema = []
    for attribute in attribute_list:
        attribute_definitions.append({'AttributeName': attribute[0],
                                     'AttributeType':attribute[1]}
                                    )
        key_schema.append({'AttributeName': attribute[0],
                          'KeyType': attribute[2]}
                         )

    db_client = boto3.client('dynamodb', region_name='us-east-1')
    db_client.create_table(
        AttributeDefinitions=attribute_definitions,
        TableName=table_name,
        KeySchema=key_schema,
        ProvisionedThroughput={
        'ReadCapacityUnits': read_capacity,
        'WriteCapacityUnits': write_capacity
        }
    )

if __name__ == '__main__':
    table_name = 'siteDict'
    attribute_list = [('name', 'S', 'HASH'), ('rank', 'N', 'RANGE')]
    create_table(table_name, attribute_list)
