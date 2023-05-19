import requests
import spacy
from typing import List
from apikey import unsplash_access_key
from .progress_utils import celery

UNSPLASH_API_KEY = unsplash_access_key

nlp = spacy.load("en_core_web_sm")


def search_unsplash(query: str, count: int = 10) -> List[dict]:
    url = "https://api.unsplash.com/search/photos"
    params = {
        "query": query,
        "client_id": UNSPLASH_API_KEY,
        "per_page": count,
    }
    response = requests.get(url, params=params)

    if response.status_code != 200:
        raise Exception("Failed to fetch images from Unsplash")

    data = response.json()
    return [result["urls"] for result in data["results"]]

def get_unsplash_image_urls(query: str, count: int = 10) -> List[str]:
    results = search_unsplash(query, count)
    return [result["regular"] for result in results]

def extract_nouns(text):
    doc = nlp(text)
    return [chunk.text for chunk in doc.noun_chunks]

@celery.task(bind=True)
def fetch_image_urls(self, data):
    print("HERE IS DATA", data)
    chunks = data['chunks']
    print("HERE IS PROMPT", chunks)
    prompt = ' '.join(chunks)
    # Extract nouns from the prompt
    nouns = extract_nouns(prompt)
    # Use the first noun as the query
    query = nouns[0] if nouns else ''
    image_urls = get_unsplash_image_urls(query, count=10)
    # Return the original data and the image URLs
    return {'data': data, 'image_urls': image_urls}