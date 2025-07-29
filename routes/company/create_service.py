from flask import Blueprint, jsonify, request
from config import firebase_service

CREATE_SERVICE = Blueprint("CREATE_SERVICE", __name__)

@CREATE_SERVICE.route("/create_service", methods=["POST"])
def create_service():
    try:
        data = request.json
        db = firebase_service.db

        # Crear servicio en Firestore
        doc_ref = db.collection("servicios").add({
            "id": data["service"]["id"],
            "businessId": data["service"]["businessId"],
            "name_service": data["service"]["name_service"],
            "description": data["service"]["description"],
            "duration": data["service"]["duration"],
            "price": data["service"]["price"],
            "active": data["service"]["active"],
            "capacity": data["service"]["capacity"],
            "requiresSpecificEmployee": data["service"]["requiresSpecificEmployee"],
            "allowedEmployeeIds": data["service"]["allowedEmployeeIds"] or [],
            "requiresDeposit": data["service"]["requiresDeposit"],
            "paymentPercentage": data["service"]["paymentPercentage"],
            "schedule": data["service"]["schedule"],
            "blackoutDates": data["service"]["blackoutDates"] or [],
        })
        
        doc_id = doc_ref[1].id
        created_service = db.collection("servicios").document(doc_id).get().to_dict()

        if not doc_ref:
            return jsonify({"status": 404, "details": "No se pudo crear el servicio"}), 404

        return jsonify({"status": 200, "details": created_service}), 200

    except Exception as e:
        print("error",str(e))
        return jsonify({"status": 500, "error": str(e)}), 500
