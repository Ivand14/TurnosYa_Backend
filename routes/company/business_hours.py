from flask import Blueprint, jsonify, request
from config import firebase_service

BUSINESS_HOURS = Blueprint("BUSINESS_HOURS", __name__)

@BUSINESS_HOURS.route("/business_hours", methods=["POST"])
def business_hours():
    try:
        data = request.get_json()
        db = firebase_service.db
        
        business_hours_ref = db.collection("horarios_atencion").add({
            "id": data["id"],
            "day": data["day"],
            "startTime": data["startTime"],
            "endTime": data["endTime"],
            "businessId": data["businessId"]
        })
        
        if not business_hours_ref:
            return jsonify({
            "status": 404,  
            "details": "Error al crear horarios",
            })
        
        return jsonify({
            "status": 200,  
            "details": "Horarios creados",
        })
        
    except Exception as e:
        return jsonify({
                "status":500,
                "details": f"Error al buscar la empresa: {str(e)}"
            })