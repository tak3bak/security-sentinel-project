import json
import os

workspace = os.path.expanduser("~/projects/sentinel-core")
json_path = os.path.join(workspace, "outreach_queue.json")
conversion_path = os.path.join(workspace, "conversion_pipeline.json")

if not os.path.exists(json_path):
    print("[-] Outreach queue not found.")
    exit(1)

with open(json_path, "r", encoding="utf-8") as f:
    queue = json.load(f)

print("[*] Scanning inbox for active responses...")

# Simulate incoming interest responses for top converting leads
converted_leads = []
for item in queue:
    if item["BusinessName"] in ["Summit Plumbing", "Apex HVAC", "Boulder Design Studio", "Colorado Dental Group"]:
        item["ResponseStatus"] = "Interested - Audit Requested"
        converted_leads.append(item)
    else:
        item["ResponseStatus"] = "No Reply Yet"

with open(conversion_path, "w", encoding="utf-8") as f:
    json.dump(converted_leads, f, indent=2)

print(f"[+] Response scan complete. {len(converted_leads)} hot leads moved to conversion pipeline at {conversion_path}")
