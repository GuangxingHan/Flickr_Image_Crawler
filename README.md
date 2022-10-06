# Flickr_Image_Crawler
A tool to crawl Flickr images

The tool supports downloading image urls of all galleries from a flickr user, and provides a simple BoW based text-matching method for matching flickr image titles/desscriptions to a pre-defined database.

The code is used to build an artwork dataset for instance-level recognition. For more details, please visit https://ilr-workshop.github.io/ECCVW2020/ and https://ilr-workshop.github.io/ICCVW2021/

The project page of our NeurIPS 2021 Datasets and Benchmarks Track paper: 'The Met Dataset: Instance-level Recognition for Artworks' is [here](http://cmp.felk.cvut.cz/met/)

# Citing Our Work
If you use this tool/dataset in your research, please use the following BibTeX entries:
```
@inproceedings{ypsilantis2021met,
  title={The met dataset: Instance-level recognition for artworks},
  author={Ypsilantis, Nikolaos-Antonios and Garcia, Noa and Han, Guangxing and Ibrahimi, Sarah and Van Noord, Nanne and Tolias, Giorgos},
  booktitle={Thirty-fifth Conference on Neural Information Processing Systems Datasets and Benchmarks Track (Round 2)},
  year={2021}
}
```

## Acknowledgement

[Python Flickr API](https://github.com/alexis-mignon/python-flickr-api) is used to build our Flickr Crawler.

[NLTK](https://www.nltk.org/) and [fuzzywuzzy](https://github.com/seatgeek/fuzzywuzzy) are used for text preprocessing.
