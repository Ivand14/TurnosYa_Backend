import os
from flask import Blueprint, jsonify,redirect
import mercadopago
from dotenv import load_dotenv
import uuid
import requests
load_dotenv()

ACCESS_TOKEN = os.getenv("MP_ACCESS_TOKEN_PROD")
MP_CLIENT_ID = os.getenv("MP_CLIENT_ID")
redirect_uri = "https://turnosya-backend.onrender.com/callback"


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

@USER_AUTHORIZATION.route("/mercado_pago/salesman", methods=["GET"])
def conect_to_salesman():
    client_id = os.getenv("MP_CLIENT_ID")
    print("clientid",client_id)
    randomId = uuid.uuid4()
    auth_url = f"https://www.mercadopago.com.ar/auth/authorize?client_id={client_id}&response_type=code&platform_id=mp&state={randomId}&redirect_uri={redirect_uri}"
    return redirect(auth_url)


@USER_AUTHORIZATION.route("/mercado_pago/token", methods=["GET"])
def obtener_access_token(code):
    token_url = "https://api.mercadopago.com/oauth/token"
    payload = {
        "client_id": MP_CLIENT_ID,
        "client_secret": os.getenv("MP_CLIENT_SECRET"),
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": redirect_uri
    }

    response = requests.post(token_url, data=payload)
    return response.json()  

