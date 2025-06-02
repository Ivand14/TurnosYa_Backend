from flask import Blueprint, jsonify, request
from config import firebase_service

DELETE_SCHEDULE = Blueprint("DELETE_SCHEDULE", __name__)

@DELETE_SCHEDULE.route("/delete_schedule", methods=["DELETE"])
def delete_schedule():
    try:
        data = request.json
        schedule_id = data.get("id")  

        if not schedule_id:
            return jsonify({"error": "ID requerido"}), 400

        db = firebase_service.db
        doc_ref = db.collection("horarios").where("id", "==", schedule_id)
        doc_snapshot = doc_ref.stream()

        doc_list = list(doc_snapshot)  # Convertir a lista para verificar existencia

        if not doc_list:  
            return jsonify({"status": 404, "details": "Horario no encontrado"}), 404

        # Eliminar cada documento encontrado
        for doc in doc_list:
            doc.reference.delete()

        return jsonify({"status": 200, "message": "Horario eliminado correctamente"}), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
