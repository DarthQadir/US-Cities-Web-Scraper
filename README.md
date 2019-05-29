## US Cities Web Scraper in Python3

Scraper that extract data about US cities from a wikipedia page

### Libraries used
* BeautifulSoup/bs4
* csv
* requests

### How to run

You can simply run the code since I've given the functions appropriate inputs for the names of the CSV files.

It takes a few minutes depending on your computer and internet connection to parse the elevation data from each city's wikipedia page.

The output should be 3 csv files:
* One without the additional elevation data
* One without the additional elevation data but has a column for elevation
* One with the additional data 


### Functions in the code

* remove_unicode
  * Filters out unicode characters from the HTML
* get_data
  * Uses the GET request from the requests library to get data from a url
* parser
  * Parses and filters the HTML data according to the HTML element and class specified
* csv_formatter
  * Formats the data to be written to a csv file. For example, the land area and population density columns have two data cells
* write_csv
  * Writes data to a csv file. The name is specified by the user
* add_col
  * Adds a new column to your csv file
* add_data
  * Adds data for the new column
  
