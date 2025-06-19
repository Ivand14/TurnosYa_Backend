import os
from flask import Blueprint, jsonify, redirect, request
from dotenv import load_dotenv
import requests
from config.firebase_service import db

load_dotenv()

AUTH_URL = "https://auth.mercadopago.com/authorization"
CLIENT_ID = os.getenv("MP_CLIENT_ID")
CLIENT_SECRET = os.getenv("MP_CLIENT_SECRET")
REDIRECT_URI = "https://turnosya-backend.onrender.com/oauth/callback"
redirect_url = f"{AUTH_URL}?client_id={CLIENT_ID}&response_type=code&redirect_uri={REDIRECT_URI}"

USER_AUTHORIZATION = Blueprint("USER_AUTHORIZATION", __name__)

@USER_AUTHORIZATION.route("/mercado_pago")
def mercado_pago():
    business_id = request.args.get("businessId")
    redirect_url = f"{AUTH_URL}?client_id={CLIENT_ID}&response_type=code&redirect_uri={REDIRECT_URI}&state={business_id}"
    return redirect(redirect_url)


@USER_AUTHORIZATION.route("/oauth/callback")
def oauth_callback():
    authorization_code = request.args.get("code")
    businessId = request.args.get("state")

    if not authorization_code:
        return jsonify({"error": "No se recibió código de autorización"}), 400

    access_token = get_access_token(authorization_code, businessId)
    if not access_token:
        return jsonify({"error": "No se pudo obtener access token"}), 400

    # HTML con redirección suave
    return f"""
    <!DOCTYPE html>
    <html lang="es">
      <head>
        <meta charset="UTF-8" />
        <title>Conectando con tu cuenta...</title>
        <style>
          body {{
            font-family: sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            background-color: #f5f5f5;
          }}
          .spinner {{
            border: 4px solid #f3f3f3;
            border-top: 4px solid #3498db;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            animation: spin 1s linear infinite;
            margin-right: 12px;
          }}
          @keyframes spin {{
            0% {{ transform: rotate(0deg); }}
            100% {{ transform: rotate(360deg); }}
          }}
        </style>
      </head>
      <body>
        <div style="text-align:center;">
          <div style="display:flex; justify-content:center; align-items:center; margin-bottom:1rem;">
            <div class="spinner"></div>
            <h3 style="margin:0;">Redirigiendo al panel de empresa...</h3>
          </div>
          <p>Un momento por favor</p>
        </div>
        <script>
          setTimeout(function() {{
            window.location.href = "http://localhost:8080/admin-dashboard/{businessId}";
          }}, 1800);
        </script>
      </body>
    </html>
    """


    
    
def get_access_token(authorization_code, businessId):
    '''Obtener y guardar el Access Token del vendedor en Firestore'''
    
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
    access_token_data = response.json()

    print("access_token_data", access_token_data)

    if "access_token" not in access_token_data:
        return jsonify({
            "error": "No se pudo obtener access token",
            "details": access_token_data
        }), 400

    # Buscar empresa en Firestore
    business_query = db.collection("empresas").where("id", "==", businessId)
    docs = business_query.get()

    empresa_doc = list(docs)

    if not empresa_doc:
        return jsonify({"error": "Empresa no encontrada"}), 404

    for doc in empresa_doc:
        doc.reference.update({
            "mercado_pago": {
                "user_id": access_token_data["user_id"],
                "access_token": access_token_data["access_token"],
                "refresh_token": access_token_data["refresh_token"],
                "expires_in": access_token_data["expires_in"],
                "public_key": access_token_data["public_key"],
                "live_mode": access_token_data["live_mode"]
            },
            "mercado_pago_connect":True
        })

    return jsonify({
        "message": "Token del vendedor registrado con éxito",
        "status": 200
    })



