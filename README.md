# Neurolabs Image Recognition Pipeline & Analytics

This project implements an end-to-end computer vision pipeline using the
**Neurolabs Image Recognition API**.
It covers the full workflow:

1.  Fetch image-recognition tasks
2.  Submit image URLs to tasks
3.  Retrieve per-image detection results
4.  Store JSON results locally
5.  Normalise COCO-format outputs into a DataFrame
6.  Join detections with `/catalog-items` metadata
7.  Build analytics (product distribution, brand distribution,
    confidence stats)
8.  Export charts and cleaned datasets

## 🚀 Features

-   Image recognition API pipeline
-   JSON saving
-   COCO parsing
-   Catalog metadata enrichment
-   Analytics + chart generation
-   Clean folder structure

## 📁 Project Structure

    NEUROLABS/
    ├── .env
    ├── requirements.txt
    ├── README.md
    ├── src/
    │   ├── api_client.py
    │   ├── pipeline.py
    │   ├── utils.py
    ├── data/
    │   └── results_json/
    ├── notebooks/
    │   ├── analysis.ipynb
    │   ├── analysis_utils.py
    │   ├── chart_generator.py
    │   └── outputs/
    │       ├── df_joined.csv
    │       ├── df_products_only.csv
    │       └── charts/

## 🔧 Installation

### 1. Clone repo

    git clone https://github.com/juderob-dev/neurolabs.git
    cd neurolabs

### 2. Create environment

    python3 -m venv .venv
    source .venv/bin/activate

### 3. Install dependencies

    pip install -r requirements.txt

### 4. Create `.env`

    NEUROLABS_API_KEY=your_api_key_here
    BASE_URL=add_base_here

### 4. Create `data/` folder 
    Create 2 folders in the data folder
    input_urls/ and results_json/ folder
    In the input_urls folder add your cooler.csv and your ambient.csv

    In your results_json folder create 2 more folders
    ambient_results/ and cooler_results/



## ▶️ Run Pipeline

    python src/main.py

## 📊 Run Analytics

Open:

    notebooks/analysis.ipynb

    Run All Cells

## 📈 Outputs

-   top_products.png
-   brand_distribution.png
-   confidence_hist.png
-   df_joined.csv
-   df_products_only.csv
