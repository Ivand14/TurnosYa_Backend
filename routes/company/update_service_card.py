from flask import Blueprint, jsonify, request
from config import firebase_service

UPDATE_SERVICE_CARD = Blueprint("UPDATE_SERVICE_CARD", __name__)

@UPDATE_SERVICE_CARD.route("/update_service_card/<id>", methods=["PATCH"])
def update_service_card(id):
    data = request.json
    db =  firebase_service.db
    
    print(data)

    try:
        update_service_ref = db.collection("servicios").where("id","==",id)
        update_service_docs = update_service_ref.stream()
        
        service_list = list(update_service_docs)

        if not service_list:
            return jsonify({"status": 404, "details": "Horario no encontrado"}), 404

        for doc in service_list:
            doc.reference.update({
                "name": data["name_service"],
                "description": data["description"],
                "duration": data["duration"],
                "price": data["price"],
                "capacity": data["capacity"],
                "requiresSpecificEmployee": data["requiresSpecificEmployee"],
                "allowedEmployeeIds": data["allowedEmployeeIds"],
                "schedule": data["schedule"] or [],
                "blackoutDates": data["blackoutDates"] or [],
            })

        
        updated_service = [{"id": doc.id, **doc.to_dict()} for doc in service_list]


        return jsonify({"status": 200, "details": updated_service}), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500