import os
import requests
import csv
import json
import pandas as pd

def fetch_url_with_data(url, custom_headers, data):
    try:
        response = requests.post(url, headers=custom_headers, json=data)
        if response.status_code == 200:
            
            response_dict = response.json() 
            
            # Pretty Printing JSON string back 
            print(json.dumps(response_dict, indent=4, sort_keys=True))
            return response.json()
        else:
            print("Error:", response.status_code)
            return None
    except requests.RequestException as e:
        print("Error:", e)
        return None

def extract_classification(json_response):
    if "text_classifications" in json_response:
        for classification in json_response["text_classifications"]:
            if "model_classifications" in classification:
                for model_classification in classification["model_classifications"]:
                    return model_classification["classifications"]
    return None

def extract_behavior(json_response):
    results = []

    # Iterate through the detections
    for detection in json_response.get("detections", []):
        # Iterate through the behaviors in each detection
        for behavior in detection.get("behaviors", []):
            name = behavior.get("name")
            confidence = behavior.get("confidence")
            results.append((name, confidence))
    
    return results

    return None

def write_classification_to_csv(classification, input_text, output_file):
    if classification:
        with open(output_file, 'a', newline='') as file:
            writer = csv.writer(file)
            if file.tell() == 0:
                writer.writerow(["Input Text", "Behavior", "Probability"])
            for c in classification:
    
                    writer.writerow([
                        input_text,
                        c[0],
                        c[1]
                    ])

        # print(f"Classification appended to CSV: {output_file}")
    # else:
        # print("No classification found for 'azcs' model.")

def write_behaviors_to_csv(behaviors, input_text, output_file):
    if behaviors:
        print(behaviors)
        with open(output_file, 'a', newline='') as file:
            writer = csv.writer(file)
            if file.tell() == 0:
                writer.writerow(["Input Text", "Category", "Probability"])
            for behavior in behaviors:
                    name, confidence = behavior
    
                    writer.writerow([
                        input_text,
                        name,
                        confidence
                    ])

        # print(f"Classification appended to CSV: {output_file}")
    # else:
        # print("No classification found for 'azcs' model.")

if __name__ == "__main__":
    url = "https://api.mpathic.ai/v1/classifications"
    output_file = "coredata/classifications.csv"

    # url = "https://api.mpathic.ai/v1/behaviors"
    # output_file = "coredata/behaviors.csv"
    # Get Bearer token from environment variable
    bearer_token = os.environ.get("BEARER_TOKEN")
    
    if not bearer_token:
        print("Error: BEARER_TOKEN environment variable is not set.")
    else:
        # print ("BEARER_TOKEN environment variable is set.")
        headers = {
            "mpathic-id": "885085b47e2446b49b3bc5895267eae7",
            # "mpathic-profile": "de58f2ef6ff74e64bb597519e284ab7f    ",
            "mpathic-profile": "d6aa92ca765b4083a11e2616b708e934",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {bearer_token}"
        }
        
        # Read input data from CSV
        datadir = "annomi"
        datatype = "csv"

        for file in os.listdir(datadir):
            if file.endswith(datatype):
                froot = file.split(".")[0]
                print(f"xls {file} -> {froot}")
                if datatype == "csv":
                    df = pd.read_csv(f"{datadir}/{file}")
                    # rename utterance_text to text
                    df.rename(columns = {'utterance_text':'text'}, inplace = True)
                # Load the Excel file
                if datatype == "xlsx":
                    df = pd.read_excel(f"{datadir}/{file}")
                os.makedirs(f"{datadir}/classresults", exist_ok=True)
                output_file = f"{datadir}/classresults/{froot}_classifications-retool.csv"

                # Extract the 'text' column
                text_column = df['text'].tolist()
                for text in text_column:
                    data = {
                        "input": text,
                        "include_behaviors": True
                    }
                    json_response = fetch_url_with_data(url, headers, data)
                    if json_response:
                        classification = extract_behavior(json_response)
                        print(f"Classification: {classification}")
                        # write_behaviors_to_csv(classification, text, output_file)
                        write_classification_to_csv(classification, text, output_file)
                    else:
                        print("Failed to fetch URL or extract classification.")

        # input_csv_file = "coredata/input_data.csv"
        # with open(input_csv_file, newline='') as csvfile:
        #     reader = csv.DictReader(csvfile)
        #     for row in reader:
        #         input_text = row["text"]
        #         # print(f"Input text: {input_text}")
        #         data = {
        #             "input": input_text,
        #             "include_behaviors": True
        #         }
        #         json_response = fetch_url_with_data(url, headers, data)
        #         if json_response:
        #             classification = extract_behavior(json_response)
        #             print(f"Classification: {classification}")
        #             write_behaviors_to_csv(classification, input_text, output_file)
        #         else:
        #             print("Failed to fetch URL or extract classification.")
