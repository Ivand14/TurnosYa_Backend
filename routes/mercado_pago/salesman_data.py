from flask import jsonify,Blueprint
from config.firebase_service import db
import requests

SALESMAN_DATA = Blueprint("SALESMAN_DATA",__name__)

@SALESMAN_DATA.route("/salesman/<businessId>",methods=["GET"])
def salesman_data(businessId):
    mp_data = db.collection("empresas").where("id","==",businessId).stream()
    
    access_token = None
    
    for doc in mp_data:
        business = doc.to_dict()
        if "mercado_pago" not in business:
            jsonify({
                "status":400,
                "message":"Esta cuenta no esta vinculada a mercado pago"
            })
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
        })

    return jsonify({
        "status": 200,
        "details": response.json()
    })