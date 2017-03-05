from collections import OrderedDict
import requests
from bs4 import BeautifulSoup
from timer import timethis


# Thing that change:
# base_url, login_url, whether login is needed.
# how the site is parsed
# Things that stay the same:
# need to get listings, and output as a list of sites.

class ListingsRetriever:
    """
    Class for retrieving top listings from Alexa.
    """
    BASE_URL = "http://www.alexa.com/topsites/global;"
    LOGIN_URL = "http://www.alexa.com/secure/login/ajaxex"

    def __init__(self, email, password, num_sites=100):
        self.email = email
        self.password = password
        self.num_sites = num_sites
        self.num_pages = self._get_number_of_amazon_pages(num_sites)

    def get_listings(self):
        """
        Return a list of the top Alexa sites.
        """
        print("Retrieving top sites from Alexa...")
        soupy_listings = self._get_soupy_listings()
        top_sites = self._scrub_listings(soupy_listings)
        print("Top sites retrieved...")
        return top_sites

    def _get_number_of_amazon_pages(self, num_sites):
        """
        Return the number of amazon pages to visit.

        num_sites: the number of sites to retrieve.

        Since there are 25 results per page,
        and a user might want a number of results
        that is not a multiple of 25,
        this method ensures
        that any desired results over the multiple
        are still retrieved.

        It's not necessary for the naive implementation
        but it will make future enhancements easier
        by maintaining abstraction.
        """
        if num_sites % 25 == 0:
            return num_sites // 25
        else:
            return (num_sites // 25) + 1

    def _get_soupy_listings(self):
        """
        Return a list of site listings,
        still made of soup.
        """
        with requests.Session() as s:
            payload = {'email': self.email, 'password': self.password, 'async': 'async', "type": "object"}
            p = s.post(self.LOGIN_URL, data=payload)
            # need to visit a second time to get a successful login.
            p = s.post(self.LOGIN_URL, data=payload)
            soupy_listings = []
            for number in range(self.num_pages):
                page = s.get(self.BASE_URL + str(number))
                soup = BeautifulSoup(page.text, 'html.parser')
                listings_table = soup.find("div", "listings table")
                page_listings = listings_table.find_all("div", "site-listing")
                soupy_listings.extend(page_listings)
            return soupy_listings

    def _scrub_listings(self, soupy_listings):
        """
        Return a list of sites
        equal in number to self.num_sites.

        soupy_listings: a list of site listings strained from the soup.
        """
        sites = []
        for listing in soupy_listings[:self.num_sites]:
            description = listing.find("div", "td DescriptionCell")
            unclean_site = description.p.get_text()
            scrubbed_site = unclean_site.strip()
            sites.append(scrubbed_site)
        return sites

# things that change:
# nothing if this is the data we're retrieving.
# I may want to handle cases where the protocol is included by default though,
# and add some try-except blocks to handle those cases.
# Reportbuilder.py should handle any list of dictionaries.
# This means that an entirely different class could work wth it,
# e.g. getting data from an API or from a different type of file.

class SiteRetriever:
    """
    Class for retrieving data from a list of sites.
    """
    def build_sites_list(self, listings):
        """
        Return a list of site dictionaries.

        listings: a list of websites without their protocols.
        """
        print("Collecting sites data...")
        sites_list = []
        for site in listings:
            print("Collecting {0}'s data...".format(site))
            # need event invocation lambda to run here.
            # This means moving the logic between this and 'the next comment'
            # into its an event lambda to call asynchronously.
            # and instead of returning a sites list, I should store the list of dicts in a dynamoDB.
            try:
                page = self._get_page(site)
                sites_list.append(self._build_site_dictionary(page, site))
            except requests.exceptions.ConnectionError:
                print("{0} could not be accessed".format(site))
                continue
            ##### the next comment

        print("Sites data collected.")
        return sites_list
        # I can access the list of dicts from the db to pass to the reportbuilder.
        # reportbuilder shouldn't be responsible for the retrieval.


    @timethis
    def _build_site_dictionary(self, page, site):
        """
        Return a site dictionary.

        page: a response object from a website.
        site: a url without a protocol.
        """
        headers, cookies, word_count = self._get_data_from(page)
        return {
            "site_name": site,
            "headers": headers,
            "cookies": cookies,
            "word_count": word_count}

    def _get_data_from(self, page):
        """
        Return all of the data retrieved from page.

        page: A response object from a website.
        """
        headers = list(page.headers.keys())
        cookies = page.cookies.keys()
        word_count = self._get_wordcount(page)
        return (headers, cookies, word_count)

    def _get_page(self, site):
        """
        Return a response object from the site.

        site: a url without a protocol.
        """
        try:
            url = "http://" + site
            page = requests.get(url)
        except requests.exceptions.SSLError:
            url = "http://www." + site
            page = requests.get(url)
        return page


    def _get_wordcount(self, page):
        """
        Return the number of words on a page.

        page: A response object from a website.
        """
        soup = BeautifulSoup(page.text, 'html.parser')
        words = soup.get_text().split()
        return len(words)
