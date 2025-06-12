from flask import Blueprint,request,jsonify
# from config.firebase_service import db
# from config.socket_config import socketio
from dotenv import load_dotenv
import requests
load_dotenv()
import os
# import uuid


USER_AUTHORIZATION = Blueprint("USER_AUTHORIZATION",__name__)

@USER_AUTHORIZATION.route("/mercado_pago_authorization", methods=["GET"])
def mercado_pago_user_authorization():
    client_id = os.environ.get("MP_CLIENT_ID")
    client_secret = os.environ.get("MP_CLIENT_SECRET")
    if not client_id:
        return jsonify({"error": "Client ID no encontrado"}), 400

    code = request.args.get("code")
    token_url = "https://api.mercadopago.com/oauth/token"
    payload = {
        "client_id": client_id,
        "client_secret": client_secret,
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": "https://a736-191-81-179-138.ngrok-free.app/mercadopago/callback"
    }

    response = requests.post(token_url, data=payload)
    data = response.json()
    return data 
