The python file `crawlStreetViewAPI.py` can be used to crawl meta data from the streetview api or crawl the images.

###The file takes in the following arguments:
-i path to the input csv file delimited with semicolons, each row must have the following columns lat,lon,heading
-m path to where to write the metadata csv file
-k the google API key
-d path to where to download streetview images, if -d is not specificed it means the code will download metadata only 


### The following is an example of running the code on sfo_image_coords_sample.csv to get the meta data (no -d is specified, otherwise it will download images)

python3 crawlStreetViewAPI.py -i /home/fahad/git/scrapingPOI/google/streetView/data/sfo_image_coords_sample.csv -m /home/fahad/git/scrapingPOI/google/streetView/data/sfo_sample_dowloaded_metadata.csv -k SOME_KEY
