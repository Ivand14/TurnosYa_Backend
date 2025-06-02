from flask import Blueprint, jsonify, request
from config import firebase_service

GET_SCHEDULES = Blueprint("GET_SCHEDULE",__name__)

@GET_SCHEDULES.route("/all_schedule/<businessId>",methods=["GET"])
def get_schedules_company(businessId):
    db = firebase_service.db
    
    
    schedule_ref = db.collection("horarios").where("businessId","==",businessId)
    sch = schedule_ref.stream()
    all_sch = [{"id":doc.id, **doc.to_dict()} for doc in sch]
    
    if not all_sch:
        return jsonify({
            "status": 404,  
            "details": "Error al encotrar horarios",
        })
        
    return jsonify({
            "status": 200,  
            "details":all_sch,
        })