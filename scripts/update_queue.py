import csv
import json
import os

workspace = os.path.expanduser("~/projects/sentinel-core")
enriched_csv = os.path.join(workspace, "leads_enriched.csv")
json_path = os.path.join(workspace, "outreach_queue.json")

print("[*] Generating high-converting outreach queue from enriched data...")

queue = []
with open(enriched_csv, mode="r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        first_name = row["ContactPerson"].split()[0]
        business = row["BusinessName"]
        os_type = row["PrimaryOS"]
        vertical = row["Vertical"]
        
        # Tailored message incorporating vertical and OS context
        msg = f"Hey {first_name}, managing endpoints and security across your {os_type} setup for {business} usually drains time and budget with recurring software licenses. We deploy a local, modular security sentinel tailored for {vertical} teams with zero monthly fees. Want a quick 5-minute system audit?"
        
        queue.append({
            "BusinessName": business,
            "ContactPerson": row["ContactPerson"],
            "Email": row["Email"],
            "Phone": row["Phone"],
            "PrimaryOS": os_type,
            "Vertical": vertical,
            "EmployeeRange": row["EmployeeRange"],
            "RevenueTier": row["RevenueTier"],
            "Message": msg,
            "Status": "Pending"
        })

with open(json_path, mode="w", encoding="utf-8") as jf:
    json.dump(queue, jf, indent=2)

print(f"[+] Outreach queue successfully updated with {len(queue)} targeted leads at {json_path}")
