from serpapi import GoogleSearch
from apikey import serp

def get_image_results(query):
    num_results = 5  # Set the fixed value for the number of result images
    params = {
        "q": query,
        "engine": "google_images",
        "ijn": "0",
        "api_key": serp,
    }

    search = GoogleSearch(params)
    results = search.get_dict()
    images_results = results["images_results"][:num_results]  # Slice the list to get the desired number of results

    print(f"Number of image results: {len(images_results)}")

    return images_results