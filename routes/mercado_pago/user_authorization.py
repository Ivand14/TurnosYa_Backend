from flask import Blueprint, request, jsonify, redirect
import requests
from dotenv import load_dotenv
import os
load_dotenv()

CLIENT_ID = os.getenv("MP_CLIENT_ID")
CLIENT_SECRET = os.getenv("MP_CLIENT_SECRET")
REDIRECT_URI = "https://turnosya-backend.onrender.com"

USER_AUTHORIZATION = Blueprint("USER_AUTHORIZATION", __name__)

# 🔹 URL de autorización para que los vendedores se conecten
@USER_AUTHORIZATION.route("/mercado_pago_login", methods=["GET"])
def mercado_pago_login():
    return redirect(f"https://auth.mercadopago.com/authorization?client_id={CLIENT_ID}&response_type=code&redirect_uri={REDIRECT_URI}", code=302)

# 🔹 Callback que recibe el código y solicita el Access Token
@USER_AUTHORIZATION.route("/mercadopago/callback", methods=["GET"])
def mercadopago_callback():
    code = request.args.get("code")
    
    print(code)
    
    if not code:
        return jsonify({"error": "Código de autorización no recibido"}), 400

    token_url = "https://api.mercadopago.com/oauth/token"
    payload = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI
    }
    
    response = requests.post(token_url, data=payload)
    print(response)
    data = response.json()
    print(data)

    return jsonify(data)
