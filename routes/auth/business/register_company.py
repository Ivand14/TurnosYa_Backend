from flask import Blueprint, request, jsonify
from config import firebase_service
from firebase_admin import auth,storage
import requests
import os
from dotenv import load_dotenv
load_dotenv()

ACCESS_TOKEN = os.getenv("MP_ACCESS_TOKEN_PROD")

REGISTER_COMPANY = Blueprint("REGISTER_COMPANY", __name__)

@REGISTER_COMPANY.route("/register_company/<preapproval_id>", methods=["POST"])
def register_company(preapproval_id):
    data = request.form
    file = request.files.get("logo")
    company_image_url = ""
    
    if file:
        try:
            bucket = storage.bucket()
            blob = bucket.blob(f"company_profile/{file.filename}")
            blob.upload_from_string(file.read(), content_type=file.content_type)

            blob.make_public()
            company_image_url = blob.public_url
        except Exception as e:
            return jsonify({"status": 500, "details": f"Error al subir imagen: {str(e)}"}), 500
    
    if not data:
        return jsonify({"status": 400, "details": "Datos de solicitud inválidos"}), 400
    if not file:
        return {"error": "No se envió ningún archivo"}, 400
    try:
        company = auth.create_user(
            email=data.get("email"),
            password=data.get("password"),
            display_name=data.get("businessName")
        )
        
        for key,values in data.items():
            if not values:
                return jsonify({
                    "status":404,
                    "details":"Faltan campos por completar"
                })

        company_register_db = firebase_service.db.collection("empresas").add({
            "email": company.email,
            "id": company.uid,
            "company_name": company.display_name,
            "rol": "business",
            "owner": data.get("ownerName"),
            "phone": data.get("phone"),
            "company_type": data.get("businessType"),
            "address": data.get("address"),
            "description": data.get("description"),
            "logo":company_image_url,
            "subscriptionPlan": data.get("subscriptionPlan"),
            "preapproval_id":preapproval_id
        })
        

        return jsonify({"status": 200, "details": "Empresa creada con éxito"}), 200

    except Exception as e:
        return jsonify({"status": 500, "details": str(e)}), 500


@REGISTER_COMPANY.route("/updateBusiness/subscription", methods=["PATCH"])
def update_subscription():
    data = request.json
    db = firebase_service.db
    preapproval_id = data.get("preapproval_id")
    
    if not preapproval_id:
        return jsonify({
            "status":404,
            "details":"preapproval_id es necesario"
        })
    
    try:
        business_doc = db.collection("empresas").where("preapproval_id","==",preapproval_id).get()
        business_list = list(business_doc)
        
        if not business_list:
            return jsonify({
                "status":404,
                "details":"Este negocio no existe"
            })
        
        response = requests.get(
            f"https://api.mercadopago.com/preapproval/{preapproval_id}",
            headers={"Authorization": f"Bearer {ACCESS_TOKEN}"}
        )
        
        response_data = response.json() 
        
        for business in business_list:
            business.reference.update({
                "mercado_pago_subscription": {
                    "id": response_data.get("id"),
                    "status": response_data.get("status"),
                    "next_payment_date": response_data.get("auto_recurring", {}).get("next_payment_date"),
                    "reason": response_data.get("reason")
                }
            })

                
        return jsonify({"status": 200, "details": "Subscripcion actualizada con exito"}), 200
        
    except Exception as e:
        return jsonify({"status": 500, "details": str(e)}), 500