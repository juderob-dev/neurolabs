import os
import json
import pandas as pd
from dotenv import load_dotenv
import requests

# Go up one directory
load_dotenv("../.env")

API_KEY = os.getenv("NEUROLABS_API_KEY")

BASE_URL = os.getenv("BASE_URL")

headers = {
    "accept": "application/json",
    "X-API-Key": API_KEY
}

def load_catalog_items():
    """Fetch catalog items from the API and convert to a DataFrame."""
    url = f"{BASE_URL}/catalog-items?limit=100&offset=0"
    r = requests.get(url, headers=headers)

    if r.status_code >= 400:
        print("ERROR STATUS:", r.status_code)
        print("ERROR BODY:", r.text)
        print("HEADERS:", headers)
        print("URL:", url)
    r.raise_for_status()

    items = r.json().get("items", [])
    df_catalog = pd.json_normalize(items)

    return df_catalog


def load_results_from_folder(folder_path):
    rows = []

    for file_name in os.listdir(folder_path):
        if not file_name.endswith(".json"):
            continue

        with open(os.path.join(folder_path, file_name)) as f:
            data = json.load(f)

        image_url = data.get("image_url")

        coco = data.get("coco", {})
        annotations = coco.get("annotations", [])
        categories = coco.get("categories", [])

        # Build category_id → product info map
        category_map = {}
        for cat in categories:
            cid = cat["id"]
            neu = cat.get("neurolabs", {}) or {}
            category_map[cid] = {
                "product_uuid": neu.get("productUuid"),
                "product_name": neu.get("name"),
                "product_tags": neu.get("tags"),
                "category_label": cat.get("name")
            }

        # Extract annotation rows
        for ann in annotations:
            cat_id = ann["category_id"]
            bbox = ann["bbox"]
            neu = ann.get("neurolabs", {}) or {}

            row = {
                "image_url": image_url,
                "category_id": cat_id,
                "bbox": bbox,
                "area": ann.get("area"),
                "score": neu.get("score"),
                "modalities": neu.get("modalities", {}),
                "alternate_predictions": neu.get("alternative_predictions", [])
            }

            # Merge product info from category map
            product_info = category_map.get(cat_id, {})
            row.update(product_info)

            rows.append(row)

    return pd.DataFrame(rows)
