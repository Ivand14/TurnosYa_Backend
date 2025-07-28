from flask import request, jsonify, session, Blueprint
from firebase_admin import auth
from config import firebase_service

LOGIN_BP = Blueprint("Login", __name__)

@LOGIN_BP.route("/login", methods=["POST"])
def login():
    try:
        # Obtener el token del header
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith("Bearer "):
            return jsonify({"error": "Token no proporcionado o mal formado"}), 401

        token = auth_header.split("Bearer ")[1]

        # Verificar el token
        decoded_token = auth.verify_id_token(token)
        print("decoded_token:", decoded_token)

        user_id = decoded_token["user_id"]
        user_email = decoded_token["email"]
        user_name = decoded_token.get("name", "")

        # Revisar si ya existe
        users_ref = firebase_service.db.collection("usuarios")
        users_email = users_ref.get()
        existe = any(u.to_dict().get("email") == user_email for u in users_email)

        if decoded_token['firebase']['sign_in_provider'] == "google.com" and not existe:
            users_ref.add({
                "email": user_email,
                "id": user_id,
                "name": user_name,
                "rol": "user"
            })

        session["uid"] = user_id
        session["email"] = user_email

        return jsonify({'success': True, 'sessionId': user_id}), 200

    except Exception as e:
        print("Error interno:", str(e))  # <-- Muy importante para depurar
        return jsonify({'error': str(e)}), 500
