import requests
from bs4 import BeautifulSoup
import json
import google.generativeai as genai
import os


api_key = "AIzaSyCotfFeT5P1Rbr6n9IPuEgv3g10Ls5n91A"
website_url = "https://www.wsj.com/"
genai.configure(api_key=api_key)

model = genai.GenerativeModel('gemini-1.5-flash')

# Function to scrape the website and retrieve all links
def scrape_website(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    links = [a['href'] for a in soup.find_all('a', href=True)]
    return links

# Function to save webpage content and generate questions
def save_content_and_generate_questions_separately(url, content_filepath, questions_filepath, api_key):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

# Extract all text from the webpage
    content = soup.get_text()
    print(content)
    # Save the content to a JSON file
    with open(content_filepath, 'w') as file:
        json.dump({'url': url, 'content': content}, file)

    # Generate questions using the Gemini API
    questions = generate_questions(content, api_key)
    
    # Save the questions to a separate JSON file
    with open(questions_filepath, 'w') as file:
        json.dump({'url': url, 'questions': questions}, file)

# Function to generate questions using Gemini API
def generate_questions(content, api_key, n=10):
    data = {
        'model': 'gemini',  # Replace with the correct model name if applicable
        'prompt': f"Generate {n} concise questions under 80 characters from the following content:\n{content}\n",
        'max_tokens': 100  # Adjust if necessary
    }
    response = model.generate_content(f"Generate {n} concise questions under 80 characters from the following content:\n{content}\n")
    # response.raise_for_status()  # Ensure we notice bad responses

    # Extract questions from the response
    result = response.text
    print(result)
    # text = result['choices'][0]['text'].strip()
    # questions = [q.strip() for q in text.split('\n') if q.strip()]
    
    return questions

# Example usage

# Scrape the website to get all links
links = scrape_website(website_url)
# with open('link/', 'w') as file:
#     json.dump(links, file)
# For each link, save the content and generate questions in separate files
# for i, link in enumerate(links):
#     if i>10:
#         break
#     try:
#         content_filepath = f'data/page_content_{i}.json'
#         questions_filepath = f'data/page_questions_{i}.json'
#         save_content_and_generate_questions_separately(link, content_filepath, questions_filepath, api_key)
#     except Exception as e:
#         print(f"{i} Error processing {link}: {e}")
