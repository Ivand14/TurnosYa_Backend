from flask import Blueprint, request, jsonify
from config import firebase_service
from firebase_admin import auth, storage
import requests
import os
from dotenv import load_dotenv

load_dotenv()

ACCESS_TOKEN = os.getenv("MP_ACCESS_TOKEN_PROD")

REGISTER_COMPANY = Blueprint("REGISTER_COMPANY", __name__)

@REGISTER_COMPANY.route("/register_company/<preapproval_id>", methods=["POST"])
def register_company(preapproval_id):
    data = request.json

    if not data:
        return jsonify({"status": 400, "details": "Datos de solicitud inválidos"}), 400


    try:
        # Crear usuario de empresa en Firebase Authentication
        company = auth.create_user(
            email=data.get("email"),
            password=data.get("password"),
            display_name=data.get("businessName")
        )

        for key, value in data.items():
            if not value:
                return jsonify({
                    "status": 404,
                    "details": "Faltan campos por completar"
                })

        # Guardar empresa en Firestore
        company_data = {
            "email": company.email,
            "id": company.uid,
            "company_name": company.display_name,
            "rol": "business",
            "owner": data.get("ownerName"),
            "phone": data.get("phone"),
            "company_type": data.get("businessType"),
            "address": data.get("address"),
            "logo": data.get("logo_url"),
            "subscriptionPlan": data.get("subscriptionPlan"),
            "preapproval_id": preapproval_id
        }
        
        if data.get("description"):
            company_data["description"] = data.get("description")
            
        firebase_service.db.collection("empresas").add(company_data)

        # Obtener los datos de la suscripción desde Mercado Pago
        try:
            response = requests.get(
                f"https://api.mercadopago.com/preapproval/{preapproval_id}",
                headers={"Authorization": f"Bearer {ACCESS_TOKEN}"}
            )
            response_data = response.json()

            # Buscar el documento de empresa con ese preapproval_id
            business_doc = firebase_service.db.collection("empresas").where("preapproval_id", "==", preapproval_id).get()
            for business in business_doc:
                business.reference.update({
                    "mercado_pago_subscription": {
                        "id": response_data.get("id"),
                        "status": response_data.get("status"),
                        "next_payment_date": response_data.get("auto_recurring", {}).get("next_payment_date"),
                        "reason": response_data.get("reason")
                    }
                })

        except Exception as e:
            print(f"Error al obtener o guardar subscripción: {e}")

        return jsonify({"status": 200, "details": "Empresa creada con éxito"}), 200

    except Exception as e:
        return jsonify({"status": 500, "details": str(e)}), 500
