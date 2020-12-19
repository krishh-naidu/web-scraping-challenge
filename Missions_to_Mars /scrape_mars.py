# Import dependencies
from bs4 import BeautifulSoup
import requests
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd


def init_browser():
    # Note: Replace the path with your actual path to the chromedriver
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    return Browser('chrome', **executable_path, headless=False)
'''

# @NOTE: Replace the path with your actual path to the chromedriver
executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
browser = Browser('chrome', **executable_path, headless=False)'''


def scrape():
    scraped_data={}
    output=NASA_Mars_News()
    scraped_data['mars_news_title']=output[0]
    scraped_data['mars_paragraph']=output[1]
    scraped_data['mars_image']=NASA_Mars_Image()
    scraped_data['mars_facts']=NASA_Mars_Facts()
    scraped_data['mars_hemisphere']=NASA_Mars_Hemispheres()

    return scraped_data



def NASA_Mars_News():
    browser=init_browser()
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    html = browser.html
    # create a Beautifulsoup object and parse with 'html.parser'
    soup = BeautifulSoup(html,'html.parser')
    latest_news_article_title = soup.find("div", class_='list_text').find('a').text
    latest_news_article_paragraph = soup.find("div", class_='article_teaser_body').text
    output=[latest_news_article_title,latest_news_article_paragraph]
    browser.quit()
    return output

def NASA_Mars_Image():
    browser = init_browser()
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    html = browser.html
    # create a Beautifulsoup object and parse with 'html.parser'
    soup = BeautifulSoup(html,'html.parser')

    image = soup.find('div',class_='carousel_items')
    image_url = image.article['style']
    new_image_url = image_url.split(' ')[1].split("(")[1].split(" ' ")[0][1:-3]
    new_image_url
    featured_image_url = "https://www.jpl.nasa.gov" + new_image_url
    browser.quit()
    return featured_image_url

def NASA_Mars_Facts():
    browser = init_browser()
    url = 'https://space-facts.com/mars/'
    browser.visit(url)
    mars_facts = pd.read_html(url)
    mars_facts_df = pd.DataFrame(mars_facts[0])
    mars_facts_df.columns = ["Description", "Value"]
    mars_facts_html = mars_facts_df.to_html(header = False, index = False)
    browser.quit()
    return mars_facts_html

def NASA_Mars_Hemispheres():
    browser = init_browser()
    url='https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html,'html.parser')
    products = soup.find('div',id='product-section')
    items = products.find_all('div',class_='item')
    hemisphere_image_urls = []
    for item in items:
        try:
            title = item.h3.text
            title = title.replace('Enhanced','')
            end_link = item.a['href']
            image_link = "https://astrogeology.usgs.gov/" + end_link
            browser.visit(image_link)
            html = browser.html
            soup=BeautifulSoup(html, "html.parser")
            downloads = soup.find("div", class_="downloads")
            image_url = downloads.a["href"]
            hemisphere_image_urls.append({"title": title, "img_url": image_url})
        except Exception as e:
            print(e)
    browser.quit()
    return hemisphere_image_urls

