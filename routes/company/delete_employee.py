from flask import Blueprint, jsonify, request
from config import firebase_service

DELETE_EMPLOYEE = Blueprint("DELETE_EMPLOYEE", __name__)

@DELETE_EMPLOYEE.route("/delete_employee", methods=["DELETE"])
def delete_employee():
    try:
        data = request.json
        emp_id = data.get("id")  

        if not emp_id:
            return jsonify({"error": "ID requerido"}), 400

        db = firebase_service.db
        doc_ref = db.collection("employees").document(emp_id)
        # doc_snapshot = doc_ref.stream()

        # doc_list = list(doc_snapshot) 

        if not doc_ref:  
            return jsonify({"status": 404, "details": "Empleado no encontrado"}), 404

        # for doc in doc_list:
        #     doc.reference.delete()
        
        doc_ref.delete()

        return jsonify({"status": 200, "message": "Empleado eliminado correctamente"}), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
