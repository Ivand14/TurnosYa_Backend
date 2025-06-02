from flask import Blueprint, jsonify, request
from config import firebase_service

DELETE_SERVICE = Blueprint("DELETE_SERVICE", __name__)

@DELETE_SERVICE.route("/delete_service", methods=["DELETE"])
def delete_schedule():
    try:
        data = request.json
        service_id = data.get("id")  

        if not service_id:
            return jsonify({"error": "ID requerido"}), 400

        db = firebase_service.db
        doc_ref = db.collection("servicios").where("id","==",service_id)
        doc_snap = doc_ref.stream()
        
        doc_list = list(doc_snap)
        
        if not doc_list:  
            return jsonify({"status": 404, "details": "servicio no encontrado"}), 404
        
        for doc in doc_list:
            doc.reference.delete()
        
    
        return jsonify({"status": 200, "message": "Servicio eliminado correctamente"}), 200
    
    except Exception as e:
        return jsonify({"status": 500, "error": str(e)}), 500
