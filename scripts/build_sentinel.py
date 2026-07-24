import os
import csv
import json

workspace = os.path.expanduser("~/projects/sentinel-core")
print(f"[*] Initializing Sentinel Core workspace at {workspace}...")

for sub in ["linux", "macos", "windows"]:
    os.makedirs(os.path.join(workspace, sub), exist_ok=True)

# 1. Linux deploy script
linux_script = """#!/usr/bin/env bash
set -euo pipefail
LOG_FILE="/var/log/sentinel_deploy.log"
echo "[*] Starting Linux Sentinel deployment..." | tee -a "$LOG_FILE"
echo "[+] Linux deployment complete." | tee -a "$LOG_FILE"
"""
linux_path = os.path.join(workspace, "linux", "deploy.sh")
with open(linux_path, "w") as f:
    f.write(linux_script)
os.chmod(linux_path, 0o755)

# 2. macOS deploy script
macos_script = """#!/usr/bin/env bash
set -euo pipefail
LOG_FILE="/var/log/sentinel_deploy.log"
echo "[*] Starting macOS Sentinel deployment..." | tee -a "$LOG_FILE"
echo "[+] macOS deployment complete." | tee -a "$LOG_FILE"
"""
macos_path = os.path.join(workspace, "macos", "deploy.sh")
with open(macos_path, "w") as f:
    f.write(macos_script)
os.chmod(macos_path, 0o755)

# 3. Windows deploy script
win_script = """$ErrorActionPreference = "Stop"
Write-Host "[*] Starting Windows Sentinel deployment..."
Write-Host "[+] Windows deployment complete." -ForegroundColor Green
"""
win_path = os.path.join(workspace, "windows", "deploy.ps1")
with open(win_path, "w") as f:
    f.write(win_script)

# 4. Generate leads CSV
csv_data = """BusinessName,ContactPerson,Phone,Email,PrimaryOS
Summit Plumbing,John Doe,303-555-0101,john@summitplumbing.test,Windows
Apex HVAC,Jane Smith,303-555-0102,jane@apexhvac.test,Windows
Boulder Design Studio,Alice Johnson,720-555-0103,alice@boulderdesign.test,macOS
Denver Legal Partners,Robert Brown,303-555-0104,rbrown@denverlegal.test,Windows
Rocky Mountain Clinic,Dr. Emily Davis,303-555-0105,edavis@rmclinic.test,Linux
Metro Electric,Michael Wilson,303-555-0106,mwilson@metroelectric.test,Windows
Front Range Architecture,Sarah Miller,720-555-0107,smiller@frontrange.test,macOS
Mile High Roofing,David Anderson,303-555-0108,danderson@milehigh.test,Windows
Boulder Tech Solutions,Chris Thomas,720-555-0109,cthomas@bouldertech.test,Linux
Colorado Dental Group,Dr. Lisa Jackson,303-555-0110,ljackson@codental.test,Windows
A-1 Plumbing Services,Mark White,303-555-0111,mark@a1plumbing.test,Windows
Precision HVAC,Paul Harris,303-555-0112,paul@precisionhvac.test,Windows
Summit Creative,Laura Martin,720-555-0113,laura@summitcreative.test,macOS
Vanguard Legal,Brian Clark,303-555-0114,bclark@vanguardlegal.test,Windows
Alpine Medical Care,Dr. Kevin Lewis,303-555-0115,klewis@alpinemed.test,Linux
Statewide Electric,Steven Lee,303-555-0116,slee@statewide.test,Windows
Cascade Design Lab,Rachel Walker,720-555-0117,rachel@cascadedesign.test,macOS
Empire Roofing,Jason Hall,303-555-0118,jhall@empireroofing.test,Windows
Nexus Systems,Amy Allen,720-555-0119,aallen@nexussys.test,Linux
Metro Dental Care,Dr. Eric Young,303-555-0120,eyoung@metrodental.test,Windows
Quick Fix Plumbing,Scott King,303-555-0121,scott@quickfix.test,Windows
ProAir HVAC,Gary Wright,303-555-0122,gary@proair.test,Windows
Studio West,Anna Scott,720-555-0123,anna@studiowest.test,macOS
Integrity Law,Kenneth Green,303-555-0124,kgreen@integritylaw.test,Windows
Mountain View Clinic,Dr. Sandra Baker,303-555-0125,sbaker@mountainview.test,Linux
PowerLine Electric,Frank Adams,303-555-0126,fadams@powerline.test,Windows
Altitude Media,Michelle Nelson,720-555-0127,mnelson@altitudemedia.test,macOS
Peak Roofing,Jerry Carter,303-555-0128,jcarter@peakroofing.test,Windows
Core IT Consulting,Raymond Mitchell,720-555-0129,rmitchell@coreit.test,Linux
Smile Dental,Dr. Helen Perez,303-555-0130,hperez@smiledental.test,Windows"""

csv_path = os.path.join(workspace, "leads_mixed_os.csv")
with open(csv_path, "w") as f:
    f.write("\n".join([line.strip() for line in csv_data.strip().split("\n")]))

# 5. Generate outreach JSON queue
queue = []
with open(csv_path, mode="r") as f:
    reader = csv.DictReader(f)
    for row in reader:
        first_name = row["ContactPerson"].split()[0]
        os_type = row["PrimaryOS"]
        msg = f"Hey {first_name}, managing security across your {os_type} office setup usually requires paid subscriptions. We deploy a modular security sentinel with zero monthly fees. Want a quick system audit?"
        queue.append({
            "BusinessName": row["BusinessName"],
            "ContactPerson": row["ContactPerson"],
            "Email": row["Email"],
            "Phone": row["Phone"],
            "PrimaryOS": os_type,
            "Message": msg,
            "Status": "Pending"
        })

json_path = os.path.join(workspace, "outreach_queue.json")
with open(json_path, mode="w") as jf:
    json.dump(queue, jf, indent=2)

print(f"[+] Sentinel Core setup completed successfully. Outreach queue saved to {json_path}")
