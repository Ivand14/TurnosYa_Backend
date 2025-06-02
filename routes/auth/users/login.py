from flask import Flask, request, jsonify, session, Blueprint
from firebase_admin import auth
from functools import wraps
from config import firebase_service


LOGIN_BP = Blueprint("Login", __name__)


def token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'error': 'Token de autenticación requerido'}), 401

        try:
            # Verifica el token de Firebase
            decoded_token = auth.verify_id_token(token.split('Bearer ')[1])  # Remueve "Bearer "
            # Guarda la información del usuario en el contexto de la petición
            request.user = decoded_token
        except Exception as e:
            return jsonify({'error': 'Token inválido o expirado'}), 401

        return f(*args, **kwargs)
    return decorated_function


@LOGIN_BP.route("/login", methods=["POST"])
def login():
    token = request.json  # Obtén el token del cuerpo de la petición
    all_users = firebase_service.db.collection("usuarios")
    users_email = all_users.get()
        
    try:
        # Verifica el token
        decoded_token = auth.verify_id_token(token)
        print("decoded_token",decoded_token)
        # Aquí puedes buscar al usuario en tu base de datos o crear uno si no existe
        # ...
        # Crea una sesión para el usuario
        session['uid'] = decoded_token['user_id']
        session['email'] = decoded_token['email']


        if decoded_token['firebase']['sign_in_provider'] == "google.com" and not any(email.to_dict()["email"] == decoded_token["email"] for email in users_email):
            firebase_service.db.collection("usuarios").add({
                "email":session["email"],
                "id": session["uid"],
                "name": decoded_token["name"],
                "rol":"user"
            })
            return jsonify({'success': True, 'sessionId': decoded_token["user_id"]}), 200
        return jsonify({'success': True, 'sessionId': session["uid"]}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@LOGIN_BP.route('/profile')
@token_required
def profile():
    # Obtiene la información del usuario verificado desde el token
    user = request.user
    return jsonify({'email': user['email'], 'uid': user['uid']}), 200