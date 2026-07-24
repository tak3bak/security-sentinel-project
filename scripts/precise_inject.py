import re

with open('ossec_pristine.conf', 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

# Define the localfile block
json_block = """
  <localfile>
    <log_format>json</log_format>
    <location>/var/log/custom_network_scan.json</location>
  </localfile>
"""

# Insert right after the global settings or first open ossec_config tag
if "custom_network_scan.json" not in content:
    # Target the first closing global or syscheck block to keep it safely nested
    target = "</syscheck>"
    if target in content:
        content = content.replace(target, target + "\n" + json_block, 1)
    else:
        # Fallback to right after the first <ossec_config>
        content = content.replace("<ossec_config>", "<ossec_config>" + json_block, 1)

with open('ossec_final.conf', 'w', encoding='utf-8') as f:
    f.write(content)

print("[+] Successfully generated clean configuration with embedded JSON log monitoring.")
