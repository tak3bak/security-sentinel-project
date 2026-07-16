import sqlite3
import asyncio
import httpx
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
import uvicorn
from dotenv import load_dotenv

load_dotenv()

DB_PATH = "sentinel_leases.db"

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

async def check_reputation(email):
    # High ROI: Check against AbuseIPDB or similar reputation services
    print(f"DEBUG: Checking threat intel for {email}...")
    return "SAFE"

async def check_reputation(ip):
    # High-ROI: Querying AbuseIPDB to determine threat confidence
    # Replace YOUR_API_KEY with your actual AbuseIPDB key
    print(f"DEBUG: Checking reputation for IP {ip}...")
    return 0  # Placeholder: 0=Safe, 100=Threat

async def send_alert(email):
    """Sends a POST request to your alert webhook."""
    try:
        async with httpx.AsyncClient() as client:
            # Replace 'https://webhook.site/your-unique-id' with your actual target
            await client.post("https://webhook.site/your-unique-id", json={"message": f"Threat found for {email}"})
    except Exception as e:
        print(f"DEBUG: Alert failed: {e}")

async def perform_security_scan(email):
    print(f"DEBUG: Initiating deep-scan for {email}...")
    # High-ROI: Reputation Gate
    score = await check_reputation("1.1.1.1")
    if score > 50:
        print(f"ALERT: High threat score {score} for {email}! Flagging immediately.")
        conn = get_db_connection()
        conn.execute("UPDATE leases SET status = "flagged" WHERE email = ?", (email,))
        conn.commit()
        conn.close()
        return
    # Replace 'echo' and 'THREAT' with your actual tool command and arguments
    proc = await asyncio.create_subprocess_exec(
        "echo", "THREAT",
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await proc.communicate()
    
    if proc.returncode == 0:
        results = stdout.decode().strip()
        conn = get_db_connection()
        conn.execute("UPDATE leases SET scan_results = ? WHERE email = ?", (results, email))
        
        if "THREAT" in results:
            conn.execute("UPDATE leases SET status = 'flagged' WHERE email = ?", (email,))
            print(f"ALERT: Threat detected for {email}! Status set to flagged.")
            await send_alert(email)
            
        conn.commit()
        conn.close()
        print(f"DEBUG: Scan results saved for {email}")

async def security_worker():
    print("Sentinel Analysis Engine: Worker loop started.")
    while True:
        try:
            conn = get_db_connection()
            active_leases = conn.execute("SELECT email FROM leases WHERE status = 'active'").fetchall()
            for lease in active_leases:
                await perform_security_scan(lease["email"])
            conn.close()
        except Exception as e:
            print(f"Worker Error: {e}")
        await asyncio.sleep(30)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Launch the worker task
    task = asyncio.create_task(security_worker())
    yield
    # Shutdown: Clean up task
    task.cancel()

app = FastAPI(lifespan=lifespan)

@app.post("/webhooks/stripe")
async def stripe_webhook(request: Request):
    payload = await request.json()
    if payload.get("type") == "checkout.session.completed":
        session = payload.get("data", {}).get("object", {})
        customer_email = session.get("customer_email")
        conn = get_db_connection()
        conn.execute("UPDATE leases SET status = 'active' WHERE email = ?", (customer_email,))
        conn.commit()
        conn.close()
        return {"status": "success"}
    return {"status": "ignored"}

@app.get("/status/{email}")
async def get_user_status(email: str):
    conn = get_db_connection()
    user = conn.execute("SELECT status, scan_results FROM leases WHERE email = ?", (email,)).fetchone()
    conn.close()
    if user:
        return {"email": email, "status": user["status"], "last_scan": user["scan_results"]}
    return {"error": "User not found"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
