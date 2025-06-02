from flask import Blueprint,jsonify
from config import firebase_service

GET_BUSINESS_ID = Blueprint("GET_BUSINESS_ID",__name__)

@GET_BUSINESS_ID.route("/business/<id>",methods=["GET"])
def business_id(id):

    db = firebase_service.db
    
    try:
        business_ref = db.collection("empresas").where("id","==",id).limit(1)
        business_docs = business_ref.stream()
        
        schedule_ref = db.collection("horarios").where("businessId","==",id)
        schedule_docs = schedule_ref.stream()
        
        business_data = None
        business_schedules = []
        
        for business in business_docs:
            business_data = business.to_dict()
            
        business_schedules = [schedule.to_dict() for schedule in schedule_docs]
            
        
        return jsonify({
            "status":200,
            "details": {
                "business_data": business_data,
                "business_schedules": business_schedules
            }
        })

    except Exception as e:
        return jsonify({
                "status":500,
                "details": f"Error al buscar la empresa: {str(e)}"
            })