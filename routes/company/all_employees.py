from flask import Blueprint, jsonify, request
from config import firebase_service

ALL_EMPLOYEE = Blueprint("ALL_EMPLOYEE", __name__)

@ALL_EMPLOYEE.route("/all_employee/<businessId>", methods=["GET"])
def get_employees(businessId):
    db = firebase_service.db
    employees_ref = db.collection("employees").where("businessId","==",businessId)
    employees_doc = employees_ref.stream()
    
    employees = [{"id": doc.id, **doc.to_dict()} for doc in employees_doc]
    
    if not employees:
        return jsonify({
            "status": 404,  
            "details": "Error al encontrar los empleados",
        })
    return jsonify({
            "status": 201,  
            "details": employees,
        })