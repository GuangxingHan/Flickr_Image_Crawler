# Flickr_Image_Crawler
A tool to crawl Flickr images

The tool supports downloading image urls of all galleries from a flickr user, and provides a simple BoW based text-matching method for matching flickr image titles/desscriptions to a pre-defined database.

The code is used to build an artwork dataset for instance-level recognition. For more details, please visit https://ilr-workshop.github.io/ECCVW2020/ and https://ilr-workshop.github.io/ICCVW2021/


## Special Thanks

[Python Flickr API](https://github.com/alexis-mignon/python-flickr-api) is used to build our Flickr Crawler.

[NLTK](https://www.nltk.org/) and [fuzzywuzzy](https://github.com/seatgeek/fuzzywuzzy) are used for text preprocessing.
