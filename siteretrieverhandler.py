from __future__ import print_function

def lambda_handler(event, context):


    # for each site:
    # (store the length of the site in the db with some related key.)
    # iterate over and start the async request
    #   get the data
    #       build the dictionary or w/e format
    #           store the dictionary in the dynamodb
    #

    # when the dynamodb list is the correct size:
        # make the data available through a separate endpoint.
        # if the data hasn't populated, display something else.
        # maybe I can program some retry in if the response doesn't include the list.
        # if it is the list, that should get assigned to a variable
        # for use by the reportbuilder.

    # try:
    #     # put the _get_page method into a lambda to be called from here.
    #     page = self._get_page(site)
    #     # change the following line to call a separate lambda
    #     # that appends the site to a list in a dynamodb
    #     sites_list.append(self._build_site_dictionary(page, site))
    # except requests.exceptions.ConnectionError:
    #     print("{0} could not be accessed".format(site))
