from flask import Blueprint, jsonify, request
from config import firebase_service

UPDATE_SERVICE_STATUS = Blueprint("UPDATE_SERVICE_STATUS", __name__)

@UPDATE_SERVICE_STATUS.route("/update_service_status", methods=["PATCH"])
def update_service_status():
    data = request.json
    db =  firebase_service.db
    print(data)
    try:
        update_service_ref = db.collection("servicios").where("id","==",data["id"])
        update_service_docs = update_service_ref.stream()
        
        service_list = list(update_service_docs)

        if not service_list:
            return jsonify({"status": 404, "details": "Horario no encontrado"}), 404

        for doc in service_list:
            doc.reference.update({
                "status": data["status"]
            })

        
        updated_service = [{"id": doc.id, **doc.to_dict()} for doc in service_list]


        return jsonify({"status": 200, "details": updated_service}), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500