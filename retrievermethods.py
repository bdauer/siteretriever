    def get_page(site):
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

    def build_site_dictionary(page, site):
        """
        Return a site dictionary.
        page: a response object from a website.
        site: a url without a protocol.
        """
        headers, cookies, word_count = get_data_from(page)
        return {
            "site_name": site,
            "headers": headers,
            "cookies": cookies,
            "word_count": word_count}

    def get_data_from(page):
        """
        Return all of the data retrieved from page.

        page: A response object from a website.
        """
        headers = list(page.headers.keys())
        cookies = page.cookies.keys()
        word_count = get_wordcount(page)
        return (headers, cookies, word_count)

    def get_wordcount(page):
        """
        Return the number of words on a page.

        page: A response object from a website.
        """
        soup = BeautifulSoup(page.text, 'html.parser')
        words = soup.get_text().split()
        return len(words)
