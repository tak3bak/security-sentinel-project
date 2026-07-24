#!/bin/bash

MODEL="llama3"
PROMPT_FILE="nomadik_sales_agent_prompt.md"
TARGETS_FILE="prospects.csv"
OUTBOX_DIR="outbox"

if [ ! -f "$PROMPT_FILE" ]; then echo "[-] Error: $PROMPT_FILE missing."; exit 1; fi
mkdir -p "$OUTBOX_DIR"

if [ ! -f "$TARGETS_FILE" ]; then
    echo "Company,Email,Role" > "$TARGETS_FILE"
    echo "Apex Financial,cto@apexfinancial.local,CTO" >> "$TARGETS_FILE"
    echo "Summit Cloud,security@summitcloud.local,Founder" >> "$TARGETS_FILE"
fi

echo "[+] Running clean-output acquisition loop..."

tail -n +2 "$TARGETS_FILE" | while IFS=, read -r COMPANY EMAIL ROLE; do
    if [ -z "$EMAIL" ]; then continue; fi
    
    echo "[*] Processing: $COMPANY ($ROLE)"
    
    # Strict prompt injecting actual variables and banning all conversational filler
    INSTRUCTION="System Rules:\n$(cat$PROMPT_FILE)\n\nTask: Write a direct, aggressive cold email selling Nomadik Security Sentinel to the $ROLE at$COMPANY. \nConstraints:\n- Do NOT include any conversational preamble, notes, or explanations.\n- Do NOT use placeholder brackets like [Name]. Address the $ROLE directly.\n- Output ONLY the raw email body text starting with the salutation."
    
    # Generate and clean output (stripping common LLM conversational wrappers via sed/grep if needed)
    RAW_COPY=$(echo -e "$INSTRUCTION" \vert{} ollama run $MODEL)
    
    # Strip markdown code blocks or wrapper lines if generated
    CLEAN_COPY=$(echo "$RAW_COPY" | sed '/^Here is/d' | sed '/^Note:/d' | sed 's/^```.*//g')
    
    SAFE_NAME=$(echo "$COMPANY" | tr ' ' '_')
    OUTFILE="$OUTBOX_DIR/${SAFE_NAME}_${ROLE}.txt"
    
    echo "To: $EMAIL" > "$OUTFILE"
    echo "Subject: Nomadik Sentinel Deployment - $COMPANY" >> "$OUTFILE"
    echo "----------------------------------------" >> "$OUTFILE"
    echo "$CLEAN_COPY" >> "$OUTFILE"
    
    echo "[+] Clean pitch saved to: $OUTFILE"
done

echo "[+] Batch generation complete."
