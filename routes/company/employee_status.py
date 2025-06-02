from flask import Blueprint, jsonify, request
from config import firebase_service

EMPLOYEE_STATUS = Blueprint("EMPLOYEE_STATUS", __name__)

@EMPLOYEE_STATUS.route("/employee_status", methods=["PATCH"])
def employee_status():
    try:
        data = request.json
        employee_id = data.get("id")  
        new_status = data.get("status")
        
        print(employee_id,new_status)

        if not employee_id or not new_status:
            return jsonify({"error": "Falta id o status"}), 400

        db = firebase_service.db
        employee_ref = db.collection("employees").document(employee_id).get()

        if not employee_ref.exists:  # Corrección aquí
            return jsonify({"status": 404, "details": "Empleado no encontrado"}), 404

        # Actualizar el documento directamente
        employee_ref.reference.update({"status": new_status})

        updated_employee = {"id": employee_ref.id, **employee_ref.to_dict()}

        return jsonify({"status": 200, "details": updated_employee}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
