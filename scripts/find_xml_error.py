import xml.etree.ElementTree as ET
import re

file_path = 'ossec_broken.conf'

try:
    # Attempt to parse the XML tree
    ET.parse(file_path)
    print("\n[i] XML structure is valid. The error is likely a misplaced block (e.g., placed outside the main <ossec_config> tags).")
    print("\n--- Last 15 lines of ossec_broken.conf ---")
    with open(file_path, 'r') as f:
        lines = f.readlines()
        for i, line in enumerate(lines[-15:]):
            print(f"{len(lines) - 15 + i + 1}: {line.rstrip()}")
    print("------------------------------------------\n")
    
except ET.ParseError as e:
    # Catch structural XML errors and pinpoint the line
    error_msg = str(e)
    print(f"\n[!] XML Syntax Error Detected: {error_msg}")
    
    match = re.search(r'line (\d+)', error_msg)
    if match:
        line_num = int(match.group(1))
        print(f"\n--- Context around line {line_num} ---")
        with open(file_path, 'r') as f:
            lines = f.readlines()
            start = max(0, line_num - 5)
            end = min(len(lines), line_num + 5)
            for i in range(start, end):
                prefix = ">> " if i + 1 == line_num else "   "
                print(f"{prefix}{i + 1}: {lines[i].rstrip()}")
        print("-----------------------------------\n")
