from flask import Blueprint, jsonify, request
from config.firebase_service import db
import requests

PREFERENCES_MP = Blueprint("PREFERENCES_MP", __name__)

@PREFERENCES_MP.route("/payment/create_preferences/<businessId>", methods=["POST", "OPTIONS"])
def preferences_mp(businessId):
    if request.method == "OPTIONS":
        return '', 200

    data = request.json

    docs = db.collection("empresas").where("id", "==", businessId).stream()
    business_doc = next(docs, None)

    if not business_doc:
        return jsonify({"error": "Empresa no encontrada"}), 404

    access_token = business_doc.to_dict().get("mercado_pago", {}).get("access_token")
    print("access_token",access_token)
    
    if not access_token:
        return jsonify({"error": "Vendedor no conectado a MP"}), 400

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
            "success": f"https://www.uturns.lat/business/{businessId}",
            "failure": "http://https://www.uturns.lat/confirmacion?status=failure",
            "pending": "https://www.uturns.lat/confirmacion?status=pending"
        },
        "auto_return": "approved"
    }

    resp = requests.post("https://api.mercadopago.com/checkout/preferences", json=body, headers=headers)
    return jsonify(resp.json()), resp.status_code
