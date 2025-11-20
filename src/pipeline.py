from api_client import get_tasks, submit_urls, get_result
from utils import (
    load_image_from_url,
    load_json,
    save_json,
    extract_result_uuids,
    draw_annotations,
    load_image_from_url,
    clean_url
)
import os
import csv
from PIL import Image


class NeurolabsPipeline:
    def __init__(self):
        self.cooler_uuid = None
        self.ambient_uuid = None

    def load_task_uuids(self):
        print("Fetching task UUIDs...")
        tasks = get_tasks()["items"]

        for task in tasks:
            name = task["name"].lower()
            if name == "cooler":
                self.cooler_uuid = task["uuid"]
            elif name == "ambient":
                self.ambient_uuid = task["uuid"]

        print("Cooler UUID:", self.cooler_uuid)
        print("Ambient UUID:", self.ambient_uuid)

    def load_urls_from_csv(self, path):
        urls = []
        with open(path, newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                cleaned = clean_url(row["url"])
                urls.append(cleaned)
        return urls
    
    def submit(self, uuid, urls, save_path):
        print(f"\nSubmitting {len(urls)} images to task {uuid}...")
        response = submit_urls(uuid, urls)
        save_json(response, save_path)
        return response

    def fetch_results(self, uuid, submission_path, output_folder):
        os.makedirs(output_folder, exist_ok=True)
        submission = load_json(submission_path)
        result_uuids = extract_result_uuids(submission)

        print(f"Fetching {len(result_uuids)} results...")

        for r_uuid in result_uuids:
            print(f"- Fetching: {r_uuid}")
            result_data = get_result(uuid, r_uuid)
            save_json(result_data, f"{output_folder}/{r_uuid}.json")

    def visualize_cooler(self, results_folder, output_folder):
        os.makedirs(output_folder, exist_ok=True)

        for name in os.listdir(results_folder):
            if not name.endswith(".json"):
                continue

            json_path = os.path.join(results_folder, name)
            result_data = load_json(json_path)

            url = result_data["image_url"]
            annotations = result_data.get("coco", {}).get("annotations", [])

            print("Visualizing:", name)
            image = load_image_from_url(url)
            annotated = draw_annotations(image, annotations)

            out_path = os.path.join(output_folder, name.replace(".json", ".png"))
            annotated.save(out_path)

        print(f"\nSaved cooler visualizations → {output_folder}")

    def run_full_pipeline(self):
        print("\n=== Running Neurolabs Pipeline ===\n")

        # Step 1: Load tasks
        self.load_task_uuids()

        # Step 2: Load URLs
        cooler_urls = self.load_urls_from_csv("data/input_urls/cooler.csv")
        ambient_urls = self.load_urls_from_csv("data/input_urls/ambient.csv")

        # Step 3: Upload URLs
        self.submit(
            self.cooler_uuid,
            cooler_urls,
            "data/results_json/cooler_submission.json",
        )

        self.submit(
            self.ambient_uuid,
            ambient_urls,
            "data/results_json/ambient_submission.json",
        )

        # Step 4: Fetch results
        self.fetch_results(
            self.cooler_uuid,
            "data/results_json/cooler_submission.json",
            "data/results_json/cooler_results",
        )

        self.fetch_results(
            self.ambient_uuid,
            "data/results_json/ambient_submission.json",
            "data/results_json/ambient_results",
        )

        # Step 5: Visualize cooler task only
        self.visualize_cooler(
            "data/results_json/cooler_results",
            "visuals/cooler"
        )

        print("\n=== Pipeline Complete ===")
