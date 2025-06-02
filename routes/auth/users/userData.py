from flask import Blueprint, request, jsonify
from config import firebase_service

GET_USER = Blueprint("GET_USER", __name__)

@GET_USER.route("/user_data", methods=["POST"])
def user_data():
    data = request.get_json()
    print("data:", data)

    if not data or "id" not in data:
        return jsonify({"error": "Missing or invalid request data"}), 400

    user_id = data["id"]
    db = firebase_service.db  # Cliente de Firestore

    try:
        # 🔎 Primero, busca en la colección de usuarios
        user_query = db.collection("usuarios").where("id", "==", user_id).limit(1).get()
        
        if user_query:  # Si encuentra un usuario, devuelve los datos
            for doc in user_query:
                user_data = doc.to_dict()
                print("Usuario encontrado:", user_data)
                return jsonify({"status": 200, "details": "OK", "user_data": user_data}), 200

        # 🔎 Si no se encuentra como usuario, busca en empresas
        business_query = db.collection("empresas").where("id", "==", user_id).limit(1).get()
        
        if business_query:  # Si encuentra una empresa, devuelve los datos
            for doc in business_query:
                company_data = doc.to_dict()
                print("Empresa encontrada:", company_data)
                return jsonify({"status": 200, "details": "OK", "company_data": company_data}), 200

        # ❌ Si no se encuentra en ninguna colección
        return jsonify({"error": "ID not found in users or businesses"}), 404

    except Exception as e:
        print(f"Error retrieving user data: {e}")
        return jsonify({'error': str(e)}), 500
