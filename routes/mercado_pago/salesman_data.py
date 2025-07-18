from flask import jsonify, Blueprint
from config.firebase_service import db
import requests

SALESMAN_DATA = Blueprint("SALESMAN_DATA", __name__)

@SALESMAN_DATA.route("/salesman/<businessId>", methods=["GET"])
def salesman_data(businessId):
    mp_data = db.collection("empresas").where("id", "==", businessId).stream()
    
    access_token = None
    business = None

    for doc in mp_data:
        business = doc.to_dict()
        break  
    
    if not business:
        return jsonify({
            "status": 404,
            "message": "Empresa no encontrada"
        }), 404

    if "mercado_pago" not in business or "access_token" not in business["mercado_pago"]:
        return jsonify({
            "status": 400,
            "message": "Esta cuenta no está vinculada a Mercado Pago"
        }), 400

    access_token = business["mercado_pago"]["access_token"]

    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    url = "https://api.mercadopago.com/users/me"
    
    

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.RequestException as e:
        return jsonify({
            "status": 500,
            "message": "Error al consultar los datos del vendedor",
            "error": str(e)
        }), 500

    return jsonify({
        "status": 200,
        "details": response.json()
    }), 200
