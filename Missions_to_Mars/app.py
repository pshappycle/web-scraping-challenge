from bs4 import BeautifulSoup as bs
import requests
from splinter import Browser
import pandas as pd
import re
import time
import sys
from flask import Flask, render_template, jsonify, redirect
import pymongo
import scrape_mars


app = Flask(__name__)

conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)

# Define the 'MarsDB' database in Mongo
db = client.MarsDB

collection = db.scrape_mars


@app.route('/')
def home():
    
    mars_info = collection.find_one()

    print(mars_info)
    
    
    return render_template("index.html", mars_info = mars_info)


@app.route('/scrape')
def scrape():
    
    mars_facts_data = scrape_mars.scrape()

    collection.replace_one(mars_facts_data)

    return redirect("/",code=302)
    


if __name__ == "__main__":
    app.run(debug=True)
