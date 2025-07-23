import os
from flask import Blueprint, jsonify, request
from dotenv import load_dotenv
import requests
from config.firebase_service import db
from datetime import datetime 

load_dotenv()

ACCESS_TOKEN = os.getenv("MP_ACCESS_TOKEN_PROD")

SUBSCRIPTIONS = Blueprint("SUBSCRIPTIONS", __name__)

@SUBSCRIPTIONS.route("/plan", methods=["POST"])
def subscriptions():
    data = request.get_json()

    if not data.get("payer_email"):
        return jsonify({"error": "Faltan datos requeridos"}), 400

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


# https://www.mercadopago.com.ar/subscriptions/checkout/congrats?collection_id=null&collection_status=approved&preference_id=762992048-6190dfaa-a334-4b3a-8cf5-ad63a47c8d9a&payment_type=account_money&payment_id=null&external_reference=16b414b815f54d918bc0fb90e0269ca9&site_id=MLA&status=approved&