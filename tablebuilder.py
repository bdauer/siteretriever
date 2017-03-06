from __future__ import print_function
import boto3


def create_table(client, table_name, attribute_list,
                 read_capacity=4, write_capacity=4):
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


    client.create_table(
        AttributeDefinitions=attribute_definitions,
        TableName=table_name,
        KeySchema=key_schema,
        ProvisionedThroughput={
        'ReadCapacityUnits': read_capacity,
        'WriteCapacityUnits': write_capacity
        }
    )

def add_item_to_table(client, table_name, attributes):
    """
    Add an item to an existing table.
    attribute_list format: [(name, type, value)]
    """

    item = {}
    for attribute in attributes:
            item[attribute[0]] = {attribute[1]: attribute[2]}
    print(item)
    client.put_item(
        TableName=table_name,
        Item=item
    )



if __name__ == '__main__':
    db_client = boto3.client('dynamodb', region_name='us-east-1')
    table_name = 'siteDict'
    # attribute_list = [('name', 'S', 'HASH'), ('rank', 'N', 'RANGE')]
    attributes = [('site', 'S', 'google'), ('rank', 'N', "1"),
                  ('headers', 'L', [{'S':'apple'}, {'S':'pear'}])]

    add_item_to_table(db_client, table_name, attributes)
