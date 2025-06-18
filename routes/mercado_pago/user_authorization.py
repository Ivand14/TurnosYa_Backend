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
    business_id = request.args.get("businessId")
    redirect_url = f"{AUTH_URL}?client_id={CLIENT_ID}&response_type=code&redirect_uri={REDIRECT_URI}&state={business_id}"
    return redirect(redirect_url)


@USER_AUTHORIZATION.route("/oauth/callback")
def oauth_callback(businessId):
    ''''
        capturar el codigo de autorizacion
    '''
    authorization_code = request.args.get("code")
    print("authorization_code",authorization_code)
    
    if not authorization_code:
        return jsonify({"error": "No se recibió código de autorización"}), 400
    
    # Obtener Access Token con el código recibido
    access_token = get_access_token(authorization_code,businessId)
    if not access_token:
        return jsonify({"error": "No se pudo obtener access token"}), 400

    
    
def get_access_token(authorization_code,businessId):
    ''''
    Obtener el Access Token del vendedor
    '''
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
    
    print("access_token_data",access_token_data)
    
    if access_token_data and "access_token" in access_token_data and access_token_data["access_token"]:
        return jsonify({"message":"token del vendedor registrado con exito","status":200})
    
    return jsonify({
        "status":200,
        "details":access_token_data
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
