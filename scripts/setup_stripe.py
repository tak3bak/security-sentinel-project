import stripe
import os

# Initialize Stripe API key using your environment variable
stripe.api_key = os.environ.get("STRIPE_SECRET_KEY")

def setup_security_sentinel_products():
    print("Creating Security Sentinel product catalog...")

    try:
        # 1. Create Products
        product_basic = stripe.Product.create(
            name="Security Sentinel - Basic Tier",
            description="Core infrastructure monitoring and automated daily log collection."
        )
        
        product_standard = stripe.Product.create(
            name="Security Sentinel - Standard Tier",
            description="Advanced multi-framework mapping and continuous compliance alerts."
        )
        
        product_premium = stripe.Product.create(
            name="Security Sentinel - Premium Tier",
            description="Enterprise-grade security operations integration and priority support."
        )

        # 2. Create Prices (Recurring Monthly)
        price_basic = stripe.Price.create(
            product=product_basic.id,
            unit_amount=9900,  # $99.00 USD
            currency="usd",
            recurring={"interval": "month"}
        )

        price_standard = stripe.Price.create(
            product=product_standard.id,
            unit_amount=29900, # $299.00 USD
            currency="usd",
            recurring={"interval": "month"}
        )

        price_premium = stripe.Price.create(
            product=product_premium.id,
            unit_amount=79900, # $799.00 USD
            currency="usd",
            recurring={"interval": "month"}
        )

        # 3. Create Payment Links for Instant Deployment
        link_basic = stripe.PaymentLink.create(
            line_items=[{"price": price_basic.id, "quantity": 1}],
            payment_method_types=["card"]
        )
        
        link_standard = stripe.PaymentLink.create(
            line_items=[{"price": price_standard.id, "quantity": 1}],
            payment_method_types=["card"]
        )

        link_premium = stripe.PaymentLink.create(
            line_items=[{"price": price_premium.id, "quantity": 1}],
            payment_method_types=["card"]
        )

        print("\nSuccessfully Configured Stripe Integration:")
        print(f"-> Basic Payment Link: {link_basic.url}")
        print(f"-> Standard Payment Link: {link_standard.url}")
        print(f"-> Premium Payment Link: {link_premium.url}")

    except stripe.error.StripeError as e:
        print(f"\nStripe API Error: {e.user_message}")
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")

if __name__ == "__main__":
    setup_security_sentinel_products()
