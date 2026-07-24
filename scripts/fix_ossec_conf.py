import re

with open('ossec_broken.conf', 'rb') as f:
    content = f.read()

# Strip any hidden BOM or stray keystrokes before the very first XML tag
start_idx = content.find(b'<')
if start_idx != -1:
    content = content[start_idx:]

text = content.decode('utf-8', errors='ignore').replace('\r\n', '\n')

# Inject the pristine localfile block if it doesn't already exist
clean_block = """
  <localfile>
    <log_format>json</log_format>
    <location>/var/log/custom_network_scan.json</location>
  </localfile>
"""
if "custom_network_scan.json" not in text:
    text = text.replace('</ossec_config>', clean_block + '\n</ossec_config>', 1)

with open('ossec_fixed.conf', 'w') as f:
    f.write(text)

print("[+] Cleaned ossec.conf and ensured the custom localfile block is present.")
