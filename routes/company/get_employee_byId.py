from flask import Blueprint, jsonify
from config import firebase_service

GET_EMPLOYEE_BY_ID = Blueprint("GET_EMPLOYEE_BY_ID", __name__)

@GET_EMPLOYEE_BY_ID.route("/get_employee_id/<id>", methods=["GET"])
def get_employee_id(id):
    try:
        db = firebase_service.db
        doc_ref = db.collection("employees").document(id)
        doc_snapshot = doc_ref.get()

        if not doc_snapshot.exists:  
            return jsonify({"status": 404, "details": "No se encontró al empleado"}), 404

        employee = {"id": doc_snapshot.id, **doc_snapshot.to_dict()} 

        return jsonify({"status": 200, "details": employee}), 200

    except Exception as e:
        print("Error:", str(e))
        return jsonify({"status": 500, "error": str(e)}), 500
