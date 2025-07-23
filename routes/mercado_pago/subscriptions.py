import os
from flask import Blueprint, jsonify, request
from dotenv import load_dotenv
import requests
from config.firebase_service import db
from datetime import datetime 

load_dotenv()

ACCESS_TOKEN = os.getenv("MP_ACCESS_TOKEN_PROD")

SUBSCRIPTIONS = Blueprint("SUBSCRIPTIONS", __name__)

@SUBSCRIPTIONS.route("/plan", methods=["POST"])
def subscriptions():
    data = request.get_json()

    if not data.get("email"):
        return jsonify({"error": "Faltan datos requeridos"}), 400
    


    payload = {
        "reason": data.get("reason", "Suscripción mensual"),
        "auto_recurring": {
            "frequency": 1,
            "frequency_type": "months",
            "billing_day": 5,
            "billing_day_proportional": False,
            "free_trial": {
                "frequency": data.get("free_trial", 7),
                "frequency_type": "days"
            },
            "transaction_amount": data.get("amount"),
            "currency_id": "ARS"
        },
        "payment_methods_allowed": {
            "payment_types": [
                {
                    "id": "credit_card"
                }
            ]
        },
        "back_url": "https://www.uturns.lat/login"
    }

    response = requests.post(
        "https://api.mercadopago.com/preapproval",
        headers={"Authorization": f"Bearer {ACCESS_TOKEN}"},
        json=payload
    )

    response_data = response.json()

    # if "id" not in response_data:
    #     return jsonify({"error": "Error al crear suscripción", "detalle": response_data}), 500

    # business_doc = db.collection("empresas").where("id", "==", data.get("businessId")).get()
    # business_list = list(business_doc)

    # if not business_list:
    #     return jsonify({"error": "Empresa no encontrada"}), 404

    # for buss in business_list:
    #     buss.reference.update({
    #         "subscriptions": {
    #             "preapproval_id": response_data["id"],
    #             "email": data.get("email"),
    #             "estado": "pendiente", 
    #             "fecha_creacion": datetime.now()
    #         }
    #     })

    return jsonify({
        "details":response_data
    })


@SUBSCRIPTIONS.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    topic = data.get("type") or data.get("topic")
    resource_id = data.get("data", {}).get("id")

    if topic == "preapproval" and resource_id:
        response = requests.get(
            f"https://api.mercadopago.com/preapproval/{resource_id}",
            headers={"Authorization": f"Bearer {ACCESS_TOKEN}"}
        )
        info = response.json()

        # # Actualizar el estado en la empresa correspondiente
        # empresa_doc = db.collection("empresas").where("subscriptions.preapproval_id", "==", resource_id).get()
        # for doc in empresa_doc:
        #     doc.reference.update({
        #         "subscriptions.estado": info.get("status"),
        #         "subscriptions.fecha_ultima_actualizacion": datetime.now()
        #     })
        return jsonify({
            "details":info,
            "status":200
        })

    return "", 200
