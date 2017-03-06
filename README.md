The siteretriever is currently a loose confederation of scripts and lambdas. This won't make complete sense unless you've looked at [retrievegeneratereport](https://github.com/bdauer/retrievegeneratereport). This is meant as a replacement for the website scraper and site dictionary builder.

Here's the rundown:

* `apimaker.py` contains functions for programmatically creating an api using API Gateway, adding resources and methods, and linking a lambda.

* `awssiteretriever.py` contains a lambda handler. It's going to be invoked asynchronously for each of the submitted sites. It will build the site dictionaries and save them, ~~most likely to memcache via ElastiCache~~ to a dynamoDB table.

* `helpers.py` contains shared methods. Currently the only method is a pickler for saving response data I'll need later. Eventually I should probably save to s3 buckets instead, or even better, if logs are being created, retrieve the information from there.

* `lambdabuilder.py` contains functions for programmatically creating a lambda.

* `retrievermethods.py` contains functions for use by `awssiteretriever.py` to keep the code there a little cleaner.

* `sitedictbuilder.py` contains a lambda handler that gets triggered by the API, taking a list of sites and passing each as an asynchronous call to `awssiteretriever.py`. The name is confusing and should be changed. I may also have it create the ~~ElastiCache cluster~~ dynamoDB table, which would get deleted when the data is retrieved.

* `siteretriever.py` was copied from the other repo for copying functionality. It can safely be ignored.

* The initial version of this won't have performance data. I think the best metric to track, rather than timing things myself, is billable duration. That will require accessing the logs, another beast entirely, so I'll address it later. Maybe once I get that working it will be easier to think about how to access id's and arn's without resorting to locally pickled files.
