from flask import Blueprint, jsonify, request
from config import firebase_service

GET_SERVICE = Blueprint("GET_SERVICE",__name__)

@GET_SERVICE.route("/get_services/<businessId>",methods=["GET"])
def get_services(businessId):
    db = firebase_service.db
    
    try:
        services_ref = db.collection("servicios").where("businessId","==",businessId)
        serv = services_ref.stream()
        all_services = [{"id":doc.id, **doc.to_dict()} for doc in serv]
        
        if not serv:
            return jsonify({
                "status": 404,  
                "details": "Error al encotrar horarios",
            })
            
        return jsonify({
                "status": 200,  
                "details":all_services,
            })
    except Exception as e:
        print("error",str(e))
        return jsonify({"status": 500, "error": str(e)}), 500