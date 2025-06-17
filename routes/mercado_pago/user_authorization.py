import os
from flask import Blueprint, jsonify,redirect,request
import mercadopago
from dotenv import load_dotenv
import uuid
import requests
import hashlib, hmac, binascii

load_dotenv()

ACCESS_TOKEN = os.getenv("MP_ACCESS_TOKEN_PROD")
MP_CLIENT_ID = os.getenv("MP_CLIENT_ID")
redirect_uri = "https://turnosya-backend.onrender.com/callback"


USER_AUTHORIZATION = Blueprint("USER_AUTHORIZATION", __name__)

@USER_AUTHORIZATION.route("/mercado_pago", methods=["GET"])
def mercado_pago():
    try:
        sdk = mercadopago.SDK(ACCESS_TOKEN)
        request_options = mercadopago.config.RequestOptions()
        request_options.custom_headers = {
            'x-idempotency-key': uuid.uuid4().hex  # Idempotency key dinámico
        }

        payment_data = {
            "transaction_amount": 100,
            "token": "CARD_TOKEN",  # Reemplázalo con el token generado en frontend
            "description": "Payment description",
            "payment_method_id": 'visa',
            "installments": 1,
            "payer": {
                "email": 'test_user_123456@testuser.com'
            }
        }
        
        result = sdk.payment().create(payment_data, request_options)
        return jsonify(result["response"])  # Devuelve JSON en lugar de imprimir

    except Exception as e:
        return jsonify({"error": str(e)}), 500  # Manejo de errores




