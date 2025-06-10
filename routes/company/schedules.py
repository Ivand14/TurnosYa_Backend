from flask import Blueprint, jsonify, request
from config import firebase_service

SCHEDULES = Blueprint("SCHEDULE",__name__)

@SCHEDULES.route("/schedule",methods=["POST"])
def schedules_company():
    data = request.json
    db = firebase_service.db
    
    schedule_ref = db.collection("horarios").add({
        "id": data["id"],
        # "employee": data["employee"],
        # "employeeId": data["employeeId"],
        "day": data["day"],
        "startTime": data["startTime"],
        "endTime": data["endTime"],
        "businessId": data["businessId"]
    })
    
    doc_id = schedule_ref[1].id
    created_sch = db.collection("horarios_atencion").document(doc_id).get().to_dict()
    
    if not schedule_ref:
        return jsonify({
            "status": 404,  
            "details": "Error al crear horarios",
        })
        
    return jsonify({
            "status": 200,  
            "details": schedule_ref,
        })
    