import json
import os
import time

workspace = os.path.expanduser("~/projects/sentinel-core")
json_path = os.path.join(workspace, "outreach_queue.json")

if not os.path.exists(json_path):
    print("[-] Outreach queue not found.")
    exit(1)

with open(json_path, "r", encoding="utf-8") as f:
    queue = json.load(f)

print(f"[*] Starting dispatch runner for {len(queue)} leads...")

for item in queue:
    if item["Status"] == "Pending":
        # Simulate dispatch action (integrate with email/SMS API here)
        print(f"[+] Dispatching to {item['ContactPerson']} at {item['BusinessName']} ({item['Email']})...")
        item["Status"] = "Sent"
        time.sleep(0.2) # Throttle transmission

with open(json_path, "w", encoding="utf-8") as f:
    json.dump(queue, f, indent=2)

print("[+] Batch dispatch complete. All records marked as Sent in outreach_queue.json")
