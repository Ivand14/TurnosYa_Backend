from flask import Blueprint, jsonify, request
from config import firebase_service

BUSINESS_HOURS_DELETE = Blueprint("BUSINESS_HOURS_DELETE", __name__)

@BUSINESS_HOURS_DELETE.route("/business_hours_delete", methods=["DELETE"])
def business_hours():
    try:
        data = request.get_json()
        id = data.get("id")
        db = firebase_service.db
        
        if not id:
            return jsonify({"error": "ID requerido"}), 400
        
        # Consulta de los documentos que coincidan con el ID
        business_hours_ref = db.collection("horarios_atencion").where("id", "==", id)
        business_hours_doc = business_hours_ref.stream()
        
        # Convertimos el stream en lista
        business_list = list(business_hours_doc)

        # Si no se encuentra ningún horario, devolver un error 404
        if not business_list:
            return jsonify({
                "status": 404,  
                "details": "No se encontraron horarios para eliminar"
            })

        # Eliminar cada documento encontrado
        for business in business_list:
            business.reference.delete()

        return jsonify({
            "status": 200,  
            "details": "Horarios eliminados correctamente"
        })

    except Exception as e:
        return jsonify({
            "status": 500,
            "details": f"Error al eliminar horarios: {str(e)}"
        })
