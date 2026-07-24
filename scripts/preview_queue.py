import json
import os

json_path = os.path.expanduser("~/projects/sentinel-core/outreach_queue.json")

if not os.path.exists(json_path):
    print("[-] Outreach queue not found at:", json_path)
    exit(1)

with open(json_path, "r", encoding="utf-8") as f:
    queue = json.load(f)

print(f"[*] Loaded {len(queue)} leads from queue. Previewing first 3:\n")

for i, item in enumerate(queue[:3], 1):
    print(f"--- Lead {i}: {item['BusinessName']} ({item['PrimaryOS']}) ---")
    print(f"To: {item['ContactPerson']} <{item['Email']}> | {item['Phone']}")
    print(f"Message: {item['Message']}\n")
