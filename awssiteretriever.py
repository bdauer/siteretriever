from __future__ import print_function
import requests
from bs4 import BeautifulSoup
from retrievermethods import get_page, build_site_dictionary

def lambda_handler(event, context):
    site = event['site']
    try:
        page = get_page(site)
        build_site_dictionary(page, site)
        # append to dynamodb
    except requests.exceptions.ConnectionError:
        print("{0} could not be accessed".format(site))
