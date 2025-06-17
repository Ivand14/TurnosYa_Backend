from flask import Blueprint, request, jsonify, redirect
import requests
from dotenv import load_dotenv
import os
import pkce
load_dotenv()

client_id = os.getenv("MP_CLIENT_ID")
CLIENT_SECRET = os.getenv("MP_CLIENT_SECRET")
redirect_uri = "https://turnosya-backend.onrender.com"
code_verifier = pkce.generate_code_verifier(length=128)
code_challenge = pkce.get_code_challenge(code_verifier)

USER_AUTHORIZATION = Blueprint("USER_AUTHORIZATION", __name__)

# 🔹 URL de autorización para que los vendedores se conecten
@USER_AUTHORIZATION.route("/mercado_pago_login", methods=["GET"])
def mercado_pago_login():
    auth_url = f"https://auth.mercadopago.com/authorization?response_type=code&client_id={client_id}&redirect_uri={redirect_uri}&code_challenge={code_challenge}&code_challenge_method=S256"
    return redirect(f"{auth_url}")


# 🔹 Callback que recibe el código y solicita el Access Token
@USER_AUTHORIZATION.route("/mercadopago/callback", methods=["GET"])
def mercadopago_callback():
    code = request.args.get("code")
    
    print(code)
    
    if not code:
        return jsonify({"error": "Código de autorización no recibido"}), 400

    token_url = "https://api.mercadopago.com/oauth/token"
    payload = {
        "client_id": client_id,
        "client_secret": CLIENT_SECRET,
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": redirect_uri,
        "code_verifier": code_verifier
    }
    
    response = requests.post(token_url, data=payload)
    print(response)
    data = response.json()
    print(data)

    return jsonify(data)
