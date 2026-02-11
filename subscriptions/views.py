import os

from django.shortcuts import render, reverse, redirect
import stripe

# Needs to match a key in .env file.
stripe.api_key = os.environ["STRIPE_SECRET_KEY"]


def checkout(request):
    """Create Stripe checkout session."""
    checkout_session = stripe.checkout.Session.create(
        line_items=[
            {
                "price_data": {
                    "unit_amount": 1000,  # in cents
                    "currency": "cad",
                    "product_data": {
                        "name": "Pollster Subscription",
                        # "images": [ urls... ]
                    },
                },
                "quantity": 1,
            }
        ],
        mode="payment",  # or "subscriptions"
        success_url=request.build_absolute_uri(
            reverse("subscriptions:success"),
        ),
        cancel_url=request.build_absolute_uri(
            reverse("subscriptions:cancel"),
        ),
    )
    return redirect(checkout_session.url, code=303)


def success(request):
    """Show subscription success page."""
    ...


def cancel(request):
    """Show subscription cancel page."""
    ...
