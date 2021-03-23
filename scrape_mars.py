# Dependencies
from bs4 import BeautifulSoup
import requests
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": ChromeDriverManager().install()}
    return Browser("chrome", **executable_path, headless=False)

def scrape_mars():
    # get Latest Mars News
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'

    # Retrieve news page with the requests module
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Get the first story title
    first_story_title = soup.find('div', class_='content_title')
    news_title = first_story_title.text

    # Get the first story teaser text
    first_story_teaser = soup.find('div', class_='rollover_description_inner')
    news_p = first_story_teaser.text

    #get featured image
    browser = init_browser()
    jpl_url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
    browser.visit(jpl_url)
    jpl_html = browser.html
    jpl_soup = BeautifulSoup(jpl_html, 'html.parser')
    jpl_img = jpl_soup.find('a', class_="showimg fancybox-thumbs")['href']
    featured_image_url = jpl_url[:56] + jpl_img
  
    #get mars facts
    mars_facts_url = 'https://space-facts.com/mars/'
    
    #retrieve the table using pandas
    mars_tables = pd.read_html(mars_facts_url)
    mars_df = mars_tables[0]
    mars_df = mars_df.rename(columns={0: "Description", 1: "Mars"})
    mars_df = mars_df.set_index('Description')

    #convert back to html
    mars_html_table = mars_df.to_html()
    mars_html_table = mars_html_table.replace('\n','')
    mars_html_table

    #get 4 hemisphere images
    mars_geo_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(mars_geo_url)

    mars_geo_html = browser.html
    mars_geo_soup = BeautifulSoup(mars_geo_html, 'html.parser')
    results = mars_geo_soup.find('div', class_='collapsible results')
    items = results.find_all('div', class_='item')

    hemi_urls = []
    for item in items:
        hemi_urls.append(item.find('a',class_='itemLink product-item')['href'])

    hemi_page_urls = ['https://astrogeology.usgs.gov' + url for url in hemi_urls]

    pic_info = [] #this one will be the list of dictionaries

    for url in hemi_page_urls:
        browser.visit(url)
        mars_pic_html = browser.html
        mars_pic_soup = BeautifulSoup(mars_pic_html, 'html.parser')
        result = mars_pic_soup.find_all('dd')
        pic_url = result[1].find('a')['href']
        pic_name = result[1].text.replace('_',' ').replace(' enhanced.tif', ' hemisphere').title()
        pic_info.append({"title":pic_name, "img_url":pic_url})

    browser.quit()
    
    results_dict = {"news_title":news_title,
                    "news_story":news_p,
                    "feat_img":featured_image_url,
                    "mars_facts":mars_html_table,
                    "hemi_pics":pic_info
                    }

    return results_dict
