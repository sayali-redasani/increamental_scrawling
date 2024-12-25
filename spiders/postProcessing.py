import json
import csv

def json_to_csv(json_file_path, csv_file_path):
    # Read JSON data from the file
    with open(json_file_path, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
    
    # Write to CSV file
    with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)

# Input JSON file path
json_file_path = 'depth4 saved.json'  # Replace with your JSON file path
# Output CSV file path
csv_file_path = 'output_depth4_saved.csv'  # Replace with your desired CSV file path

# Convert JSON to CSV
json_to_csv(json_file_path, csv_file_path)

