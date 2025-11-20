Neurolabs Image Recognition Pipeline & Analytics

This project implements an end-to-end workflow for running image inference using the Neurolabs API, saving per-image results, and performing product-level analytics & visualizations.
It covers the full pipeline:

Fetch tasks

Submit image URLs

Retrieve inference results

Store results locally

Join detections with catalog metadata

Build analytics (pie charts, bar charts, histograms)

Export cleaned datasets & charts

🚀 Project Overview

This repository contains:

A Python backend pipeline (src/)

A complete analysis workflow in Jupyter (notebooks/)

Stored inference results (data/)

Exported analytics (notebooks/outputs/)

Chart generation utilities (chart_generator.py)

It is designed to be clean, modular, and easy to extend.

📦 Features
✔ Image Recognition Pipeline

Load image URLs from CSV

Submit URLs to Neurolabs /image-recognition/tasks/{uuid}/urls

Retrieve per-image COCO-formatted results

Save each result as JSON

✔ Data Normalization

Extract bounding boxes, categories, confidence scores

Map COCO category_id → catalog productUuid

Build clean pandas DataFrames

✔ Catalog Join

Fetch /catalog-items

Join detection results with official product metadata (name, brand, etc.)

✔ Analytics

Product distribution

Brand distribution

Model confidence statistics

Histogram & bar charts

Output tables and CSV files

✔ Reporting

All charts saved to notebooks/outputs/charts

Clean merged dataset saved to df_joined.csv

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

