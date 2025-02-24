import json
import csv
import pandas as pd

# Load JSON file
json_file = 'AI\Data\extra.json'
csv_file = 'AI\Data\extra.csv'

with open(json_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Extract data
rows = []
for item in data["extra"]:
    tag = item["tag"]
    patterns = item.get("patterns", [])
    responses = item.get("responses", [])
    
    # Ensure patterns is a list of dictionaries
    if isinstance(patterns, list):
        for pattern in patterns:
            if isinstance(pattern, dict) and "pattern" in pattern and "response" in pattern:
                rows.append([tag, pattern["pattern"], pattern["response"]])
            elif isinstance(pattern, str) and responses:
                rows.append([tag, pattern, responses[0]])  # Map string patterns to first response

# Write to CSV
with open(csv_file, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(["tag", "pattern", "response"])  # Header
    writer.writerows(rows)

print(f"CSV file saved to {csv_file}")