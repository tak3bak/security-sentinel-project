import csv, os, subprocess, re

model, prompt_file, targets_file, outbox = "llama3", "nomadik_sales_agent_prompt.md", "prospects.csv", "outbox"

if not os.path.exists(prompt_file):
    exit("[-] Error: nomadik_sales_agent_prompt.md missing.")

os.makedirs(outbox, exist_ok=True)

if not os.path.exists(targets_file):
    with open(targets_file, "w", newline="") as f:
        f.write("Company,Email,Role\nApex Financial,cto@apexfinancial.local,CTO\nSummit Cloud,security@summitcloud.local,Founder\n")

with open(prompt_file, "r") as f:
    prompt = f.read()

print("[+] Initializing scrubbed single-block execution...")

with open(targets_file, "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        if not row["Email"]: continue
        
        print(f"[*] Processing: {row['Company']} ({row['Role']})")
        
        payload = (
            f"System Rules:\n{prompt}\n\n"
            f"Task: Write ONE single, highly aggressive, custom cold email selling Nomadik Security Sentinel to the {row['Role']} at {row['Company']}.\n"
            f"Strict Constraints:\n"
            f"- Output ONLY ONE email body starting with 'Hi {row['Role']},'.\n"
            f"- Do NOT use bracketed placeholders like [industry/field]."
        )
        
        res = subprocess.run(["ollama", "run", model], input=payload, text=True, capture_output=True)
        raw_text = res.stdout
        
        # 1. Strip preamble
        match = re.search(r'(?i)\b(hi|dear)\b', raw_text)
        if match:
            raw_text = raw_text[match.start():]
            
        # 2. Truncate subsequent options
        raw_text = re.split(r'(?i)\*\*Email\s*2\*\*|Email\s*2:|---', raw_text)[0]
            
        # 3. Clean up metadata markers
        for marker in ["* Recipient:", "Let me know", "Here is", "Note:"]:
            idx = raw_text.find(marker)
            if idx != -1:
                raw_text = raw_text[:idx]
                
        clean_copy = raw_text.strip()
        
        # 4. Strip model sign-offs
        for signoff in ["Best,", "Sincerely,", "Regards,", "Cheers,", "Best regards,"]:
            if signoff in clean_copy:
                clean_copy = clean_copy.split(signoff)[0].strip()
                break
                
        # 5. Programmatically strip ANY leftover bracketed placeholders
        clean_copy = re.sub(r'\[.*?\]', '', clean_copy)
        clean_copy = re.sub(r' +', ' ', clean_copy)  # Normalize spacing
        
        clean_copy += "\n\nBest,\nKalen"
        
        path = f"{outbox}/{row['Company'].replace(' ', '_')}_{row['Role']}.txt"
        with open(path, "w", encoding="utf-8") as out:
            out.write(f"To: {row['Email']}\n")
            out.write(f"Subject: Nomadik Sentinel Deployment - {row['Company']}\n")
            out.write(f"----------------------------------------\n")
            out.write(clean_copy + "\n")
            
        print(f"[+] Scrubbed email saved to: {path}")

print("[+] Batch complete.")
