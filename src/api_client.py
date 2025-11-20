import requests
import os
from dotenv import load_dotenv
from utils import batch_list
import time

load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))


API_KEY = os.getenv("NEUROLABS_API_KEY")
BASE_URL = os.getenv("BASE_URL")

headers = {
    "accept": "application/json",
    "X-API-Key": API_KEY
}

def submit_urls(task_uuid, url_list, batch_size=2):
    """
    Submit a list of image URLs to a specific task.
    Returns the API response containing result UUIDs.
    """
    results = []

    for batch_num, batch in enumerate(batch_list(url_list, batch_size), start=1):
        print(f"Submitting batch {batch_num} with {len(batch)} URLs...")

        payload = {"urls": batch}
        url = f"{BASE_URL}/image-recognition/tasks/{task_uuid}/urls"

        retries = 3
        for attempt in range(retries):
            response = requests.post(url, json=payload, headers=headers)

            if response.status_code == 429:
                wait = 2 ** attempt
                print(f"Rate limited. Waiting {wait} seconds before retry...")
                time.sleep(wait)
                continue

            response.raise_for_status()
            results.append(response.json())
            break

        else:
            raise Exception(f"Failed batch {batch_num} after {retries} retries")

        time.sleep(15)

    return results

def get_tasks():
    """Return all tasks in the account."""
    print(f"base: {BASE_URL}, {headers}")
    url = f"{BASE_URL}/image-recognition/tasks?limit=50&offset=0"
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

def get_result(task_uuid, result_uuid):
    """
    Retrieve a single inference result.
    """
    print(f"base: {BASE_URL}")
    url = f"{BASE_URL}/image-recognition/tasks/{task_uuid}/results/{result_uuid}"
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

