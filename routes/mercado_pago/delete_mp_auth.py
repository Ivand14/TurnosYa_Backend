from flask import Blueprint, jsonify, request
from config.firebase_service import db
from firebase_admin import firestore

DELETE_MP_AUTH = Blueprint("DELETE_MP_AUTH", __name__)

@DELETE_MP_AUTH.route("/delete/mp", methods=["DELETE"])
def delete_mp_auth():
    try:
        data = request.get_json()
        business_id = data.get("businessId")
        
        if not business_id:
            return jsonify({"status": "error", "message": "Falta businessId"}), 400

        business = db.collection("empresas").where("id", "==", business_id).get()

        if not business:
            return jsonify({"status": "error", "message": f"No se encontró empresa con ID {business_id}"}), 404

        for buss in business:
            buss.reference.update({
                "mercado_pago": firestore.DELETE_FIELD,
                "mercado_pago_connect": False
            })

        return jsonify({
            "status": "success",
            "message": "Datos de Mercado Pago eliminados correctamente"
        }), 200

    except Exception as e:
        return jsonify({
            "status": "error",
            "details": f"Error interno: {str(e)}"
        }), 500
