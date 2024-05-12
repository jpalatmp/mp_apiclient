import os
import requests
import csv

def fetch_url_with_data(url, custom_headers, data):
    try:
        response = requests.post(url, headers=custom_headers, json=data)
        if response.status_code == 200:
            return response.json()
        else:
            print("Error:", response.status_code)
            return None
    except requests.RequestException as e:
        print("Error:", e)
        return None

def extract_azcs_classification(json_response):
    if "text_classifications" in json_response:
        for classification in json_response["text_classifications"]:
            if "model_classifications" in classification:
                for model_classification in classification["model_classifications"]:
                    if model_classification["model_name"] == "azcs":
                        return model_classification["classifications"]
    return None

def write_classification_to_csv(classification, input_text, output_file):
    if classification:
        with open(output_file, 'a', newline='') as file:
            writer = csv.writer(file)
            if file.tell() == 0:
                writer.writerow(["Input Text", "Category", "Probability", "Confidence", "Prediction", "Severity", "Status", "Reason"])
            for category, details in classification.items():
                if details.get("severity") > 0:
                    writer.writerow([
                        input_text,
                        category,
                        details.get("prediction", ""),
                        details.get("severity", ""),
                    ])

        print(f"Classification appended to CSV: {output_file}")
    else:
        print("No classification found for 'azcs' model.")

if __name__ == "__main__":
    url = "https://api.mpathic.ai/v1/classifications"
    output_file = "classification.csv"
    
    # Get Bearer token from environment variable
    bearer_token = os.environ.get("BEARER_TOKEN")
    
    if not bearer_token:
        print("Error: BEARER_TOKEN environment variable is not set.")
    else:
        print ("BEARER_TOKEN environment variable is set.")
        headers = {
            "mpathic-id": "8b50976223da400c98ccf20747adca76",
            "mpathic-profile": "e1ce1f78153545f2b5bb2f2c4aabfb0d",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {bearer_token}"
        }
        
        # Read input data from CSV
        input_csv_file = "input_data.csv"
        with open(input_csv_file, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                input_text = row["text"]
                print(f"Input text: {input_text}")
                data = {
                    "input": input_text,
                    "include_behaviors": True
                }
                json_response = fetch_url_with_data(url, headers, data)
                if json_response:
                    classification = extract_azcs_classification(json_response)
                    write_classification_to_csv(classification, input_text, output_file)
                else:
                    print("Failed to fetch URL or extract classification.")
