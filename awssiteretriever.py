from __future__ import print_function
import requests
from retrievermethods import get_data_from
from tablebuilder import add_item_to_table

def lambda_handler(event, context):
    site = event['site']
    rank = event['rank']
    try:
        page = get_page(site)
        headers, cookies, word_count = get_data_from(page)
        site_data = ('site', 'S', site)
        rank_data = ('rank', 'N', str(rank))

        headers_for_db = []
        for header in headers:
            headers_for_db.append({'S': header})
        headers_data = ('headers', 'L', headers_for_db)

        cookies_data = ('cookies', 'L', cookies)
        word_count_data = ('word_count', 'N', str(word_count))
        attributes = [page_data, headers_data, cookies_data,
                 word_count_data, site_data, rank_data]

        client = boto3.client('dynamodb', region_name='us-east-1')
        table_name = "siteDict"
        add_item_to_table(client, table_name, attributes)

    except requests.exceptions.ConnectionError:
        print("{0} could not be accessed".format(site))
