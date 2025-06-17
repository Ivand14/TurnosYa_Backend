import os
from flask import Blueprint, jsonify, redirect, request
import mercadopago
from dotenv import load_dotenv
import requests

load_dotenv()

AUTH_URL = "https://auth.mercadopago.com/authorization"
CLIENT_ID = os.getenv("MP_CLIENT_ID")
CLIENT_SECRET = os.getenv("MP_CLIENT_SECRET")
REDIRECT_URI = "https://turnosya-backend.onrender.com/oauth/callback"
redirect_url = f"{AUTH_URL}?client_id={CLIENT_ID}&response_type=code&redirect_uri={REDIRECT_URI}"

USER_AUTHORIZATION = Blueprint("USER_AUTHORIZATION", __name__)

@USER_AUTHORIZATION.route("/mercado_pago")
def mercado_pago():
    return redirect(redirect_url)

# 1️⃣ Capturar el código de autorización
@USER_AUTHORIZATION.route("/oauth/callback")
def oauth_callback():
    authorization_code = request.args.get("code")
    if not authorization_code:
        return jsonify({"error": "No se recibió código de autorización"}), 400
    
    # Obtener Access Token con el código recibido
    access_token = get_access_token(authorization_code)
    if not access_token:
        return jsonify({"error": "No se pudo obtener access token"}), 400

    return jsonify({"access_token": access_token})

# 2️⃣ Obtener el Access Token del vendedor
def get_access_token(authorization_code):
    url = "https://api.mercadopago.com/oauth/token"
    data = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "authorization_code",
        "code": authorization_code,
        "redirect_uri": REDIRECT_URI
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    response = requests.post(url, data=data, headers=headers)
    return response.json().get("access_token")

# 3️⃣ Crear pago con el Access Token del vendedor
@USER_AUTHORIZATION.route("/oauth/create-payment", methods=["POST"])
def create_payment():
    access_token = request.json.get("access_token")  # Recibir el token del vendedor
    if not access_token:
        return jsonify({"error": "Falta access token"}), 400
    
    sdk = mercadopago.SDK(access_token)
    payment_data = {
        "transaction_amount": 100,
        "token": "TOKEN_GENERADO",
        "description": "Compra de prueba",
        "payment_method_id": "visa",
        "payer": {
            "email": "comprador@email.com"
        }
    }
    payment = sdk.payment().create(payment_data)
    return jsonify(payment["response"])
