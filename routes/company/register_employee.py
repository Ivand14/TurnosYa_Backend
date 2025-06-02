from flask import Blueprint, jsonify, request
from config import firebase_service

CREATE_EMPLOYEE = Blueprint("CREATE_EMPLOYEE", __name__)

@CREATE_EMPLOYEE.route("/new_employee", methods=["POST"])
def create_employee():
    data = request.get_json()  
    db = firebase_service.db
    
    print(data)

    if not data or "businessId" not in data:  
        return jsonify({
            "status": 400,  
            "details": "Faltan datos o businessId"
        })

    try:
        
        new_employee_ref = db.collection("employees").add({
            "name": data["name"],
            "email": data["email"],
            "phone": data["phone"],
            "position": data["position"],
            "businessId": data["businessId"],
            "status":"active" 
        })
        
        print(new_employee_ref)

        return jsonify({
            "status": 201,  
            "details": "Empleado creado con éxito",
        })

    except Exception as e:
        return jsonify({
            "status": 500,
            "details": f"Error al crear empleado: {str(e)}"
        })
