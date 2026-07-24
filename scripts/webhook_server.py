from fastapi import FastAPI, Request, HTTPException, Header
import stripe
import os

app = FastAPI()

# Initialize Stripe API keys and webhook secret
stripe.api_key = os.environ.get("STRIPE_SECRET_KEY")
STRIPE_WEBHOOK_SECRET = os.environ.get("STRIPE_WEBHOOK_SECRET")

def provision_client_workspace(customer_email, subscription_tier):
    print(f"[PROVISIONING] Setting up secure workspace for {customer_email} - Tier: {subscription_tier}")
    # TODO: Add your containerized environment provisioning / database mapping logic here
    pass

@app.post("/webhook")
async def stripe_webhook(request: Request, stripe_signature: str = Header(None)):
    payload = await request.body()

    if not STRIPE_WEBHOOK_SECRET:
        raise HTTPException(status_code=500, detail="Webhook secret is not configured")

    try:
        event = stripe.Webhook.construct_event(
            payload, stripe_signature, STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail="Invalid payload")
    except stripe.error.SignatureVerificationError as e:
        raise HTTPException(status_code=400, detail="Invalid signature")

    # Access event properties safely via native dot notation
    if event.type == "checkout.session.completed":
        session = event.data.object

        # Extract customer email safely
        customer_email = getattr(session, "customer_email", None)
        if not customer_email and hasattr(session, "customer_details") and session.customer_details:
            customer_details = session.customer_details
            customer_email = customer_details.get("email") if isinstance(customer_details, dict) else getattr(customer_details, "email", None)

        session_id = getattr(session, "id", None)
        
        tier_name = "Standard"
        if session_id:
            try:
                line_items = stripe.Checkout.Session.list_line_items(session_id)
                if line_items and len(line_items.data) > 0:
                    tier_name = line_items.data[0].description
            except Exception as e:
                print(f"[WARNING] Could not fetch line items: {e}")

        # Trigger automated backend provisioning
        provision_client_workspace(customer_email, tier_name)

    return {"status": "success"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
