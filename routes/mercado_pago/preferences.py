from flask import Blueprint,jsonify,request
from config.firebase_service import db
from flask_cors import CORS
import requests

PREFERENCES_MP = Blueprint("PREFERENCES_MP",__name__)
CORS(PREFERENCES_MP, origins=["http://localhost:8080","https://turno-ya-ivand14s-projects.vercel.app","https://turno-ya.vercel.app/"])


@PREFERENCES_MP.route("/payment/create_preferences/<businessId>",methods=["POST","OPTIONS"])
def preferences_mp(businessId):
    data = request.json
    
    docs = db.collection("empresas").where("id","==",businessId).stream()
    business_doc = next(docs, None)
    
    access_token = business_doc.to_dict().get("mercado_pago", {}).get("access_token")
    
    if not access_token:
        return jsonify({"error": "Vendedor no conectado a MP"}), 400
    
    if not docs:
        jsonify({
            "status":500,
            "message":"Empresa no encontrada"
        })

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    body = {
        "items": [
            {
                "title": data.get("title"),
                "quantity": 1,
                "unit_price": float(data.get("price", 100)),
                "currency_id": "ARS"
            }
        ],
        "back_urls": {
            "success": "http://localhost:8080/confirmacion?status=success",
            "failure": "http://localhost:8080/confirmacion?status=failure",
            "pending": "http://localhost:8080/confirmacion?status=pending"
        },
        "auto_return": "approved"
    }

    resp = requests.post("https://api.mercadopago.com/checkout/preferences", json=body, headers=headers)
    return jsonify(resp.json()), resp.status_code