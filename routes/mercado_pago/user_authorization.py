import os
from flask import Blueprint, jsonify
import mercadopago
from dotenv import load_dotenv
load_dotenv()

ACCESS_TOKEN = os.getenv("MP_ACCESS_TOKEN_PROD")


USER_AUTHORIZATION = Blueprint("USER_AUTHORIZATION", __name__)

@USER_AUTHORIZATION.route("/mercado_pago", methods=["GET"])
def mercado_pago_login():
    sdk = mercadopago.SDK(ACCESS_TOKEN)
    preference_data = {
      # the "purpose": "wallet_purchase", allows only logged in payments
      # to allow guest payments, you can omit this property
        "purpose": "wallet_purchase",
        "items": [
            {
                "title": "My Item",
                "quantity": 1,
                "unit_price": 75  # item unit price
            }
        ]
    }

    preference_response = sdk.preference().create(preference_data)
    preference = preference_response["response"]
    return jsonify({"details":preference})

