import os
from flask import Blueprint, jsonify, request
from dotenv import load_dotenv
import requests

load_dotenv()

ACCESS_TOKEN = os.getenv("MP_ACCESS_TOKEN_PROD")

SUBSCRIPTIONS = Blueprint("SUBSCRIPTIONS", __name__)

@SUBSCRIPTIONS.route("/plan", methods=["POST"])
def subscriptions():
    data = request.get_json()

    payload = {
        "reason": data.get("reason", "Suscripción mensual"),
        "auto_recurring": {
            "frequency": 1,
            "frequency_type": "months",
            "billing_day": 5,
            "billing_day_proportional": False,
            "free_trial": {
                "frequency": data.get("free_trial", 7),
                "frequency_type": "days"
            },
            "transaction_amount": data.get("amount"),
            "currency_id": "ARS"
        },
        "payment_methods_allowed": {
            "payment_types": [
                { "id": "credit_card" },
                { "id": "debit_card" },
                { "id": "account_money" }
            ]
        },
        "back_url": "https://www.uturns.lat/register-business"
    }

    response = requests.post(
        "https://api.mercadopago.com/preapproval_plan",
        headers={"Authorization": f"Bearer {ACCESS_TOKEN}"},
        json=payload
    )

    response_data = response.json()

    return jsonify({
        "init_point": response_data.get("init_point"),
        "preapproval_id": response_data.get("id"),
        "status": 200
    })

