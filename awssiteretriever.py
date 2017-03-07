from __future__ import print_function
import requests
import boto3
from retrievermethods import get_data_from, get_page, build_list_for_db
from tablebuilder import add_item_to_table

def lambda_handler(event, context):
    site = event['site']
    rank = event['rank']
    try:
        page = get_page(site)
        headers, cookies, word_count = get_data_from(page)

        site_data = ('name', 'S', site)
        rank_data = ('rank', 'N', str(rank + 1))
        headers_data = build_list_for_db('headers', headers, 'S')
        cookies_data = build_list_for_db('cookies', cookies, 'S')
        word_count_data = ('word_count', 'N', str(word_count))

        attributes = [site_data, rank_data, headers_data,
                      cookies_data, word_count_data]

        client = boto3.client('dynamodb', region_name='us-east-1')
        table_name = "siteDict"
        item_name = site
        add_item_to_table(client, table_name, item_name, attributes)

    except requests.exceptions.ConnectionError:
        print("{0} could not be accessed".format(site))
