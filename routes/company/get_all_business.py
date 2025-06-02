from flask import Blueprint, request, jsonify
from config import firebase_service

ALL_BUSINESS = Blueprint("ALL_BUSINESS", __name__)

@ALL_BUSINESS.route("/all_business", methods=["GET"])
def get_all_business():
    db = firebase_service.db
    try:
        empresas_ref = db.collection("empresas")
        docs = empresas_ref.stream()  # Itera sobre los documentos
        
        # Transformar cada documento en un diccionario antes de serializar
        empresas = [{"id": doc.id, **doc.to_dict()} for doc in docs]

        return jsonify({
            "status": 200,
            "detail": "ok",
            "data": empresas  # Ahora es una lista de diccionarios serializables
        })
    except Exception as e:
        print(f'Error: {str(e)}')
        return jsonify({
            "status": 500,
            "detail": str(e)
        })
