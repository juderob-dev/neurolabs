import csv
import json
import os
from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO
import matplotlib.pyplot as plt

def load_image_from_url(url):
    """Download image from a URL and load it as a PIL Image."""
    response = requests.get(url)
    response.raise_for_status()
    return Image.open(BytesIO(response.content)).convert("RGB")


def draw_annotations(image, annotations):
    draw = ImageDraw.Draw(image)

    for ann in annotations:
        bbox = ann.get("bbox", [])
        modalities = ann.get("neurolabs", {}).get("modalities", {})

        if len(bbox) == 4:
            x, y, w, h = bbox
            x1 = x
            y1 = y
            x2 = x + w
            y2 = y + h

            # Draw rectangle
            draw.rectangle([x1, y1, x2, y2], outline="red", width=3)

            # Build label text
            if modalities:
                label = ", ".join([f"{k}: {v}" for k, v in modalities.items()])
            else:
                label = ""

            # Draw label background + text
            if label:
                bbox_text = draw.textbbox((0,0), label)
                text_w = bbox_text[2] - bbox_text[0]
                text_h = bbox_text[3] - bbox_text[1]

                draw.rectangle([x1, y1 - text_h, x1 + text_w, y1], fill="red")
                draw.text((x1, y1 - text_h), label, fill="white")

    return image


def load_image_urls(csv_path):
    urls = []
    
    with open(csv_path, newline="") as f:
        reader = csv.DictReader(f)
        
        for row in reader:
            raw_url = row["url"]
            
            if not raw_url:
                continue

            # Clean the URL:
            clean_url = raw_url.strip().strip("<>").strip()

            # Only append if it's non-empty
            if clean_url:
                urls.append(clean_url)

    return urls

def save_json(data, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        json.dump(data, f, indent=2)


def batch_list(items, batch_size):
    """Yield successive batches of size batch_size."""
    for i in range(0, len(items), batch_size):
        yield items[i:i + batch_size]

def load_json(path):
    with open(path) as f:
        return json.load(f)

def extract_result_uuids(submission_json):
    """
    Takes the submission response and returns all result_uuid values.
    """
    result_uuids = []
    for batch in submission_json:
        if isinstance(batch, list): 
            for uuid in batch:
                result_uuids.append(uuid)

    return result_uuids

def clean_url(url):
    # Remove <> if present
    return url.strip().lstrip("<").rstrip(">")
