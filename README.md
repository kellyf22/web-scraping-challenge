# Web Scraping Homework - Mission to Mars

In this assignment, I built a web application that scrapes various websites for data related to Mars and displays the information in a single HTML page. 

## Step 1 - Scraping

I completed my initial scraping using Jupyter Notebook, BeautifulSoup, Pandas, and Requests/Splinter.

### NASA Mars News

* Scraped from the [NASA Mars News Site](https://mars.nasa.gov/news/) for the latest News Title and Paragraph Text.

### JPL Mars Space Images - Featured Image

* From the JPL Featured Space Image [here](https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html).

* I used splinter to navigate the site and find the image url for the current Featured Mars Image.

### Mars Facts

* Some facts from the Mars Facts webpage [here](https://space-facts.com/mars/)-- I used Pandas to scrape the table containing facts about the planet including Diameter, Mass, etc, and convert the data back to an html string.

### Mars Hemispheres

* Visit the USGS Astrogeology site [here](https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars) to obtain high resolution images for each of Mar's hemispheres.

* This required clicking each of the links to the hemispheres in order to find the image url to the full resolution image, and then saving both the image url string and the hemisphere name in a Python dictionary to store the data.

- - -

## Step 2 - MongoDB and Flask Application

Next I used MongoDB with Flask templating to create a new HTML page that displays all of the information that was scraped in the step above.

* I started by converting my Jupyter notebook into a Python script with a function that executes all of the scraping code from above and returns one Python dictionary containing all of the scraped data.

* Next, I created a route that imports my scraping script and calls my scraping function. The return value is stored in Mongo as a Python dictionary.

* Then, I created a root route `/` that will query my Mongo database and pass the mars data into an HTML template to display the data.

* Finally, I created a template HTML file called `index.html` that will take the mars data dictionary and display all of the data in the appropriate HTML elements. 
