from flask import Blueprint, jsonify, request
from config import firebase_service
from config.socket_config import socketio
from flask_socketio import emit

UPDATE_BUSINESS_SCHEDULE = Blueprint("UPDATE_BUSINESS_SCHEDULE", __name__)

@UPDATE_BUSINESS_SCHEDULE.route("/update_business_hours", methods=["PATCH"])
def update_business_hours():
    """ Maneja la actualización desde una solicitud HTTP """
    data = request.json
    db = firebase_service.db


    try:
        update_business_ref = db.collection("horarios_atencion").where("id", "==", data["id"])
        update_business_docs = update_business_ref.get()
        
        business_list = list(update_business_docs)
        
        
        if not business_list:
            return jsonify({"status": 404, "details": "Horario no encontrado"}), 404

        for doc in business_list:
            doc.reference.update({
                "startTime": data["schedule"]["startTime"],
                "endTime": data["schedule"]["endTime"]
            })
            

        updated_business = [
            {"id": doc.id, **doc.reference.get().to_dict()} for doc in business_list
        ]
        

        socketio.emit("updateBusinessHrs", updated_business) 

        return jsonify({"status": 200, "details": updated_business}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


