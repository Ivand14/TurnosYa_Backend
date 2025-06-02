from flask import Blueprint, jsonify, request
from config import firebase_service

UPDATE_BUSINESS_SCHEDULE = Blueprint("UPDATE_BUSINESS_SCHEDULE", __name__)

@UPDATE_BUSINESS_SCHEDULE.route("/update_business_hours", methods=["PATCH"])
def update_business_hours():
    data = request.json
    db =  firebase_service.db
    print(data)
    try:
        update_business_ref = db.collection("horarios_atencion").where("id","==",data["id"])
        update_business_docs = update_business_ref.stream()
        
        business_list = list(update_business_docs)

        if not business_list:
            return jsonify({"status": 404, "details": "Horario no encontrado"}), 404

        for doc in business_list:
            doc.reference.update({
                "startTime": data["schedule"]["startTime"],
                "endTime": data["schedule"]["endTime"]
            })

        
        updated_business = [{"id": doc.id, **doc.to_dict()} for doc in business_list]


        return jsonify({"status": 200, "details": updated_business}), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500