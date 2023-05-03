import requests
from typing import List
from apikey import unsplash_access_key

UNSPLASH_API_KEY = unsplash_access_key


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
