##########################################
# Imports
##########################################
from flask import Flask, jsonify, render_template
from flask_pymongo import PyMongo
import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup

##########################################
# Configuration
##########################################
app = Flask(__name__)

# Mongo DB
app.config['MONGO_URI'] = "mongodb://localhost:27017/mars_db"
mongo = PyMongo(app)

##########################################
# Routes
##########################################
'''
A Route consists of several parts:
1.) A route, which denotes a specific 'path' (endpoint)
that where a certain exchange of data will occur
2.) A function below the route that will be executed
when the 'path' (endpoint) is visited (ie. via website url)
3.) Some data is returned back to the visitor (client)
'''
@app.route("/")
def default():
    return render_template('index.html')

# Scrape Mars
@app.route("/mars")
def mars():
    # Put your entire jupyter notebook scraping code in here
    # set chromedriver path
    executable_path = {'executable_path': 'C:\\Users\\Trisarah\\Desktop\chromedriver.exe'}
    # executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser("chrome", **executable_path, headless=False)

    # setup and visit url
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    # scrape the browser into soup and get title and paragraphs 
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    news_title = soup.find('div', class_='content_title').text
    news_p = soup.find('div', class_='article_teaser_body').text

    # JPL Mars space images - feature image
    # setup new url
    image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    main_url = 'https://www.jpl.nasa.gov/'
    browser.visit(image_url)

    # scrape the browser into soup and get title and paragraphs 
    images_html = browser.html
    image_soup = BeautifulSoup(images_html, 'html.parser')

    # get background-image url
    featured_image = image_soup.find('article', class_="carousel_item")['style']

    # get end of image url by finding everything in between / and '); in the featured_image variable 
    featured_image = featured_image[featured_image.find("/")+1:featured_image.find("');")]

    featured_image_url = main_url + featured_image

    ### TODO: ADD MORE SCRAPING CODE HERE

    ############# Add everything we scraped to some container dictionary
    ############# and send it to mongodb

    # create container for scraped data
    scraped_data = {}

    # add scraped information into it
    scraped_data['News Title'] = news_title
    scraped_data['News Teaser'] = news_p
    scraped_data['Featured Image'] = featured_image_url

    ### TODO: Add to mongodb

    # Return json version of our data to see!
    return jsonify(scraped_data)

# Reference example
@app.route("/movies/johnwick")
def john_wick_data():
    movieData = [
      {
        'name': 'John Wick',
        'link': 'https://www.imdb.com/title/tt2911666/?ref_=tt_sims_tti',
        'score': 7.4
      },
      {
        'name': 'John Wick Chapter 2: Wick-vizzed',
        'link': 'https://www.imdb.com/title/tt7161870/?ref_=tt_sims_tti',
        'score': 7.5
      },
      {
        'name': 'John Wick: Chapter 3 - Parabellum',
        'link': 'https://www.imdb.com/title/tt6146586/?ref_=tt_sims_tti',
        'score': 7.7
      }
    ];

    return jsonify(movieData)

##########################################
# Initialization
##########################################
if __name__ == "__main__":
    app.run()