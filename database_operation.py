

import os
PYPPETEER_CHROMIUM_REVISION = '1263111'
os.environ['PYPPETEER_CHROMIUM_REVISION'] = PYPPETEER_CHROMIUM_REVISION

import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv

from requests_html import HTMLSession
from db_connection import create_db_connection





def check_and_insert_category(category_name):
    conn = create_db_connection()
    if conn is not None:
        try:

            cursor = conn.cursor() 
          
            check_query = "SELECT * FROM categories WHERE name = %s"
            cursor.execute(check_query, (category_name,))
            result = cursor.fetchone()

            if result:
                print(f"The category '{category_name}' already exists in the table.")
                return None
            else:
                return category_name
        except Error as e:
               print("Error while connecting to MySQL", e)







def single_news_scraper(url):
    session = HTMLSession()
    try:
        response = session.get(url)
        response.html.render()

        catg = response.html.find('.print-entity-section-wrapper', first=True).text
        category = check_and_insert_category(catg)

        return category
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    finally:
        session.close()
   

if __name__ == "__main__":
    conn = create_db_connection()
    if conn is not None:
        bd_urls = [
            "https://www.prothomalo.com/politics/r3on39o429",
            "hhttps://www.prothomalo.com/politics/lsreb1179h"
            
        ]
        
        for url in bd_urls:
            result = single_news_scraper(url)
            if result is not None:
                category1 = result
                print("category new : ", category1)
                
                #process_and_insert_news_data(conn, category, news_body, images, url)
            else:
                print(f"Failed to scrape the news article from URL: {url}")


    