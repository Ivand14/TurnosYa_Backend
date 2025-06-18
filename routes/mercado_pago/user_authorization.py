import os
from flask import Blueprint, jsonify, redirect, request
import mercadopago
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
    ''''
        capturar el codigo de autorizacion
    '''
    authorization_code = request.args.get("code")
    businessId = request.args.get("state")

    
    if not authorization_code:
        return jsonify({"error": "No se recibió código de autorización"}), 400
    
    # Obtener Access Token con el código recibido
    access_token = get_access_token(authorization_code,businessId)
    if not access_token:
        return jsonify({"error": "No se pudo obtener access token"}), 400
    
    return redirect(f"http://localhost:8080/admin-dashboard/{businessId}")

    
    
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
            }
        })

    return jsonify({
        "message": "Token del vendedor registrado con éxito",
        "status": 200
    })


@USER_AUTHORIZATION.route("/oauth/create-payment", methods=["POST"])
def create_payment():
    '''
     Crear pago con el Access Token del vendedor
     '''
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
