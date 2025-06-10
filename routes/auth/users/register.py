from flask import request, Blueprint, jsonify
from firebase_admin import auth
from config import firebase_service


SIGNUP_BP = Blueprint("Register", __name__)

@SIGNUP_BP.route("/registrarse", methods=["POST"]) 
def crear_usuario():
    data = request.json
    db = firebase_service.db
    # Crear un nuevo usuario
    try:
        user = auth.create_user(
            email=data["email"],
            password=data["password"],
            display_name=data["name"]
        )
        print("user",user)
        print(f"Usuario creado exitosamente: {user.uid}")
        if user.uid:
            db.collection("usuarios").add({
                "email":user.email,
                "id": user.uid,
                "name": user.display_name,
                "rol":"user"
            })

            return jsonify({
                "status":200,
                "message":"usuario registrado en db correctamente"
            })
        return jsonify({
            "status":200,
            "details":f"{user.email} fue creado correctamente"
        })
    except auth.EmailAlreadyExistsError:
        print("El correo electrónico ya está en uso.")
        return jsonify({
            "status":"error",
            "details":"El correo electrónico ya está en uso."
        }),404
    except ValueError as e:
        # Capturamos el error específico de validación de contraseña
        print(e)
        return jsonify({
            "status":"error",
            "details":"La contraseña es muy corta."
            }), 400


    
