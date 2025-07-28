from flask import Flask, request, jsonify, session, Blueprint
from firebase_admin import auth
from functools import wraps
from config import firebase_service

LOGIN_BP = Blueprint("Login", __name__)


@LOGIN_BP.route("/login", methods=["POST"])
def login():
    token = request.headers.get('Authorization')
    decoded_token = auth.verify_id_token(token.split('Bearer ')[1])

    all_users = firebase_service.db.collection("usuarios")
    users_email = all_users.get()
        
    try:
        # Verifica el token
        decoded_token = auth.verify_id_token(token)
        print("decoded_token",decoded_token)

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

