from flask import Blueprint, request, jsonify
from config import firebase_service
from firebase_admin import auth,storage

REGISTER_COMPANY = Blueprint("REGISTER_COMPANY", __name__)

@REGISTER_COMPANY.route("/register_company", methods=["POST"])
def register_company():
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
            "logo":company_image_url
        })
        
        print(company_register_db)

        return jsonify({"status": 200, "details": "Empresa creada con éxito"}), 200

    except Exception as e:
        return jsonify({"status": 500, "details": str(e)}), 500
