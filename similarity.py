import requests
from bs4 import BeautifulSoup
import json
import google.generativeai as genai
import os
from urllib.parse import urljoin
from sentence_transformers import SentenceTransformer, util


api_key = "AIzaSyCotfFeT5P1Rbr6n9IPuEgv3g10Ls5n91A"
website_url = "https://www.wsj.com/"
genai.configure(api_key=api_key)

# Initialize the generative model
model_gemini = genai.GenerativeModel('gemini-1.5-flash')

# Initialize SentenceTransformer for similarity search
model_sentence_transformer = SentenceTransformer('all-MiniLM-L6-v2', device='cpu') 

# Function to scrape the website and retrieve all links
def scrape_website(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    links = [urljoin(url, a['href']) for a in soup.find_all('a', href=True)]
    return links

# Function to save webpage content, generate questions, and find relevant links
def save_content_and_generate_questions_separately(url, content_filepath, questions_filepath, site_map):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract all text from the webpage
    content = soup.get_text()
    
    # Save the content to a JSON file
    with open(content_filepath, 'w') as file:
        json.dump({'url': url, 'content': content}, file)

    # Generate questions using the Gemini API
    questions = generate_questions(content)
    
    # Find relevant links for each question
    relevant_links_for_questions = {}
    for question in questions:
        relevant_links = find_relevant_links(question, site_map)
        relevant_links_for_questions[question] = relevant_links


    
    # Save the questions and relevant links to a separate JSON file
    with open(questions_filepath, 'w') as file:
        json.dump({'url': url, 'questions': relevant_links_for_questions}, file)



# Function to generate questions using Gemini API
def generate_questions(content, n=10):
    response = model_gemini.generate_content(
        f"Generate {n} concise questions under 80 characters from the following content:\n{content}\n",
    )

    

    # Extract questions from the response

    # result = response.get('text', '').strip()
    # questions = [q.strip() for q in result.split('\n') if q.strip()]


    return response.text



# Function to find relevant links for each question
def find_relevant_links(question, site_map):
    question_embedding = model_sentence_transformer.encode(question, convert_to_tensor=True)
    relevant_links = []

    for url, data in site_map.items():
        print(data)
        content_embedding = model_sentence_transformer.encode(data['content'], convert_to_tensor=True)
        similarity = util.pytorch_cos_sim(question_embedding, content_embedding)
        relevant_links.append((url, similarity.item()))

    # Sort by similarity and return top 2
    relevant_links.sort(key=lambda x: x[1], reverse=True)
    return [link for link, _ in relevant_links[:2]]




# **************************
# ******** OLD STUFF HERE ************
# ************************



def getSiteMap(website_url):
    links = scrape_website(website_url)
    site_map = {}
    
    # For each link, save the content, generate questions, and find relevant links in separate files
    for i, link in enumerate(links):
        if i > 5:  # Limiting to first 6 pages for the example
            break
        try:
            content_filepath = f'data/content/page_content_{i}.json'
            questions_filepath = f'data/questions/page_questions_{i}.json'

            # Scrape content and generate questions
            save_content_and_generate_questions_separately(link, content_filepath, questions_filepath, site_map)
            
            # Update the site map after processing each page
            with open(content_filepath, 'r') as file:
                content_data = json.load(file)
                site_map[link] = {'content': content_data['content']}
        
        except Exception as e:
            print(f"{i} Error processing {link}: {e}")


getSiteMap(website_url)


    
# # Example usage

# # Scrape the website to get all links
# links = scrape_website(website_url)

# # For each link, save the content and generate questions in separate files
# for i, link in enumerate(links):
#     if i>5:
#         break
#     try:
#         content_filepath = f'data/content/page_content_{i}.json'
#         questions_filepath = f'data/questions/page_questions_{i}.json'
#         link = "https://r.jina.ai/" + link
#         save_content_and_generate_questions_separately(link, content_filepath, questions_filepath, api_key)
#     except Exception as e:
#         print(f"{i} Error processing {link}: {e}")