import requests
from bs4 import BeautifulSoup
import json
import google.generativeai as genai
import os
from urllib.parse import urljoin

def scrape_website(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    links = [urljoin(url, a['href']) for a in soup.find_all('a', href=True)]
    return links

def getSiteMap(website_url):
    links = scrape_website(website_url)
    site_map = []
    
    # For each link, save the content, generate questions, and find relevant links in separate files
    for i, link in enumerate(links):
        if i > 5:  # Limiting to first 6 pages for the example
            break
        try:
            content_filepath = f'data/content/page_content_{i}.json'
            questions_filepath = f'data/questions/page_questions_{i}.json'

            # Scrape content and generate questions
            # save_content_and_generate_questions_separately(link, content_filepath, questions_filepath, site_map)
            
            # Update the site map after processing each page
            with open(content_filepath, 'r') as file:
                content_data = json.load(file)
                site_map.append({'url':link, 'content': content_data['content']})
        
        except Exception as e:
            print(f"{i} Error processing {link}: {e}")

    return site_map