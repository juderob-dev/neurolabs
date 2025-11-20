# Neurolabs Image Recognition Pipeline & Analytics

This project implements an end-to-end computer vision pipeline using the **Neurolabs Image Recognition API**.  
It covers the full workflow:

1. Fetch image-recognition tasks  
2. Submit image URLs to tasks  
3. Retrieve per-image detection results  
4. Store JSON results locally  
5. Normalise COCO-format outputs into a DataFrame  
6. Join detections with `/catalog-items` metadata  
7. Build analytics (product distribution, brand distribution, confidence stats)  
8. Export charts and cleaned datasets

The repository contains a **pipeline**, **utilities**, and a full **Jupyter analytics notebook**.

---

## 🚀 Features

### ✔ Image Recognition Pipeline
- List tasks using `/image-recognition/tasks`
- Submit URLs via `/tasks/{task_uuid}/urls`
- Retrieve result UUIDs
- Fetch per-image `/results/{result_uuid}`
- Save JSON responses to `data/results_json/...`

### ✔ Data Normalisation
- Parse COCO-style annotations
- Map `category_id` → product UUID via `categories[].neurolabs.productUuid`
- Extract bounding boxes, scores, metadata
- Build pandas DataFrames

### ✔ Catalog Join
- Fetch `/catalog-items`
- Join catalog product metadata to detection results
- Unified dataset: product name, brand, barcode, size, packaging, image URL, bbox, score

### ✔ Analytics
- Top products
- Brand distribution
- Confidence score histogram
- Lowest-confidence detections
- Bounding box area distribution
- Save charts as `.png`

---


## Project Structure

NEUROLABS/
│
├── src/
│   ├── api_client.py          # API calls to Neurolabs
│   ├── pipeline.py            # Full inference pipeline
│   └── utils.py               # CSV loading, URL cleaning, helpers
│
├── data/
│   └── results_json/          # Raw JSON inference outputs
│
├── notebooks/
│   ├── analysis.ipynb         # Main analysis & visualization notebook
│   ├── analysis_utils.py      # JSON → DataFrame extraction helpers
│   ├── chart_generator.py     # Functions to automatically generate & save charts
│   └── outputs/
│       ├── df_joined.csv
│       ├── df_products_only.csv
│       └── charts/
│           ├── top_products.png
│           ├── confidence_hist.png
│           └── ...
│
├── .env                       # API key (not committed)
├── requirements.txt
└── README.md


🧩 Architecture (High-Level Flow)
                        +--------------------------+
                        |  /image-recognition/tasks |
                        +------------+-------------+
                                     |
                         Fetch Task UUIDs
                                     |
                                     v
+--------------------+     +---------------------+
|  image_urls.csv    | --> | Submit URLs to Task |
+--------------------+     +---------------------+
                                     |
                                     v
                        +------------------------------+
                        | Retrieve per-image results   |
                        | /tasks/{uuid}/results/{rid}  |
                        +---------------+--------------+
                                        |
                                Save result JSON files
                                        |
                                        v
                      +-------------------------------+
                      |  Parse JSON → DataFrame       |
                      |  (COCO annotations + catalog) |
                      +-------------------------------+
                                        |
                                        v
                           +----------------------+
                           |   Analytics & Charts |
                           +----------------------+

🔧 Setup & Installation
1. Clone the repo
git clone <repo-url>
cd neurolabs

2. Create a virtual environment
python3 -m venv .venv
source .venv/bin/activate

3. Install requirements
pip install -r requirements.txt

4. Create .env in project root
NEUROLABS_API_KEY=your_key_here

🏗 Running the Inference Pipeline

The inference pipeline fetches tasks, submits images, retrieves detection results, and saves JSON files.

Run:

python src/main.py


This will:

✔ load URLs
✔ clean them (removing < >)
✔ submit them in batches
✔ save JSON results in data/results_json/...

📊 Running Analytics (Jupyter Notebook)

Open:

notebooks/analysis.ipynb

Select Run All Cells

All outputs appear in:

notebooks/outputs/

📈 Example Outputs
Product Distribution

(saved to outputs/charts/top_products.png)

Confidence Histogram

(saved to outputs/charts/confidence_hist.png)

Brand Pie Chart

(saved to outputs/charts/brand_pie.png)

