from flask import Blueprint, request, jsonify
from config import firebase_service

ALL_BUSINESS_HOURS = Blueprint("ALL_BUSINESS_HOURS", __name__)

@ALL_BUSINESS_HOURS.route("/all_business_hours/<businessId>", methods=["GET"])
def get_all_business(businessId):

    db = firebase_service.db
    try:
        business_hours_ref = db.collection("horarios_atencion").where("businessId","==",businessId)
        docs = business_hours_ref.stream()  # Itera sobre los documentos
        
        # Transformar cada documento en un diccionario antes de serializar
        business_hours = [{"id": doc.id, **doc.to_dict()} for doc in docs]

        return jsonify({
            "status": 200,
            "details": business_hours  # Ahora es una lista de diccionarios serializables
        })
    except Exception as e:
        print(f'Error: {str(e)}')
        return jsonify({
            "status": 500,
            "detail": str(e)
        })
