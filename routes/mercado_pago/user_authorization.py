import os
import secrets
from flask import Blueprint, request, jsonify, redirect
import requests

client_id = os.getenv("MP_CLIENT_ID")
redirect_uri = "https://turnosya-backend.onrender.com"
state = secrets.token_hex(16) 

auth_url = f"https://auth.mercadopago.com/authorization?client_id={client_id}&response_type=code&platform_id=mp&state={state}&redirect_uri={redirect_uri}"

USER_AUTHORIZATION = Blueprint("USER_AUTHORIZATION", __name__)

@USER_AUTHORIZATION.route("/mercado_pago_login", methods=["GET"])
def mercado_pago_login():
    return redirect(auth_url)

@USER_AUTHORIZATION.route("/callback", methods=["GET"])
def mercadopago_callback():
    code = request.args.get("code")
    if not code:
        return jsonify({"error": "Código de autorización no recibido"}), 400

    token_url = "https://api.mercadopago.com/oauth/token"
    payload = {
        "client_id": client_id,
        "client_secret": os.getenv("MP_CLIENT_SECRET"),
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": redirect_uri
    }

    response = requests.post(token_url, data=payload)
    return jsonify(response.json())


@USER_AUTHORIZATION.route("/wallet_connect", methods=["GET"])
def wallet_connect():
    access_token = os.getenv("MP_ACCESS_TOKEN_PROD")  # Token de tu aplicación en Mercado Pago
    wallet_url = "https://api.mercadopago.com/v2/wallet_connect/agreements"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    payload = {
        "return_uri": "https://turnosya-backend.onrender.com/success",  # URL de retorno
        "external_flow_id": "EXTERNAL_FLOW_ID",
        "external_user": {
            "id": "user_test_123",
            "description": "Cuenta de prueba"
        },
        "agreement_data": {
            "validation_amount": 3.14,
            "description": "Vinculación de Wallet Connect"
        }
    }

    response = requests.post(wallet_url, headers=headers, json=payload)
    data = jsonify(response.json())
    print(data)
    response = requests.post(wallet_url, headers=headers, json=payload)
    data = jsonify(response.json())

    if "agreement_uri" in data:
        return redirect(data["agreement_uri"]) 

    return jsonify({"error": "No se pudo generar la vinculación"}), 400


@USER_AUTHORIZATION.route("/wallet_webhook", methods=["POST"])
def wallet_webhook():
    data = request.json
    print("Notificación recibida:", data)
    
    if data.get("status") == "approved":
        return jsonify({"message": "Wallet conectada correctamente"}), 200

    return jsonify({"error": "No se pudo conectar la billetera"}), 400

