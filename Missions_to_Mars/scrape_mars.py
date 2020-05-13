# Dependencies
from bs4 import BeautifulSoup as bs
import requests
from splinter import Browser
import pandas as pd
import re
import time
import psycopg2


   

def scrape():
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)  
    

    mars_facts_data = {}

    # Mars News
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(url)
    soup = bs(browser.html, 'html.parser')
    
    slide = soup.find('li',class_='slide')
    results = slide.find_all('div', class_="content_title")
    news_title = results[0].get_text()

    teaser = soup.find('div', class_="article_teaser_body")
    paragraph = teaser.text

    mars_facts_data['news_title'] = news_title
    mars_facts_data['news_paragraph'] = paragraph


    #JPL Mars Space Images
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    browser.find_by_id('full_image').click()
    browser.is_element_present_by_text('more info', wait_time=3)
    browser.find_link_by_partial_text("more info").click()

    soup = bs(browser.html, 'html.parser')
    initial =soup.select_one('figure.lede a img').get('src')
    space_url = f'https://www.jpl.nasa.gov{initial}'

    mars_facts_data['image'] = space_url

    #Mars Weather
    url ='https://twitter.com/marswxreport?lang=en'
    browser.visit(url)
    time.sleep(1)

    soup = bs(browser.html, 'html.parser')
    mars_weather = soup.find_all(text=re.compile('InSight'))[0]

    mars_facts_data['mars_weather'] = mars_weather

    #Mars Facts

    url = 'https://space-facts.com/mars/'
    browser.visit(url)

    table = pd.read_html(url)[0]
    table = table.rename(columns={0:'Fact',1:'Info'})
    html_table =table.to_html()

    mars_facts_data['mars_facts_table'] = html_table
    
 
    #Mars Hemispheres
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    time.sleep(1)
    lin = [0,1,2,3]

    hemisphere_image_urls = []

    for i in lin:
        hemi_dict ={}
        browser.find_by_tag('h3')[i].click()
        time.sleep(1)
        soup = bs(browser.html, 'html.parser')
        initial =soup.find('h2', class_='title')
        title = initial.text
        hemi_dict['title'] = title
        img_url = soup.select_one('img.wide-image').get('src')
        hemi_dict['img_url'] = img_url
        browser.back()
        time.sleep(1)
        hemisphere_image_urls.append(hemi_dict)

    mars_facts_data['hemisphere_img_url'] = hemisphere_image_urls

    

    return mars_facts_data

scrape()