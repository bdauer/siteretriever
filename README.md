This won't make complete sense unless you've looked at [retrievegeneratereport](https://github.com/bdauer/retrievegeneratereport). This is meant as a replacement for the website scraper and site dictionary builder. It's a very rough draft but it works.

## Instructions

After downloading the code:

1.  In your terminal, `cd` into `siteretrieverapi`.

2.  If you'd like to create a virtualenvironment, create one with `virtualenv -p python3 env`. (Activate it with `source env/bin/activate`).

3.  `pip install -r requirements.txt` will install the requirements.

4. Run `main.py` to build the API endpoints, create a dynamodb table and upload the lambdas.

5. In the AWS console, go to the API Gateway and select `siteretriever`.

6. Select `POST` and test with a dictionary of the form `{"sites": [site, ..., site]}` where site is a website e.g. google.com, facebook.com, as a string.

7. Select `GET` and test. It should return the site data from the table.

8. For cleanup, delete the `siteretriever` API, delete the lambdas (site_data_retriever, scrape_and_store, dictionary_builder), delete the `siteDict` table in dynamoDB. Delete the `site-retrieval-role` role in IAM.

## Still needed

- Roles are too permissive. They need to be tightened.

- Instead of saving info I need to a local pickled file, I should save to an s3 bucket, or get it from a log if it's available there.

- Naming and comments aren't great.

- I got this done pretty roughly. Would need to write tests for an actual implementation.

- The GET request should check to make sure that the correct number of sites have been processed, so I'd need to store the number of sites expected and check against it.

- I could use the dyamodb as a cache, and if an item was added within the past day, get the data from there instead of processing it again.

- Speaking of caches, since this is temporary storage I considered using memcache with ElastiCache but the free tier only allows for a node type that requires a vpc, which is not included in the free tier.

- I'd still need to process the GET data a little so that it would work with the other elements of the project.

- Need to recover the billable duration for retrieving each site from the logs.
