from flask import Blueprint, jsonify, request
from config import firebase_service

GET_BOOKING = Blueprint("GET_BOOKING", __name__)

@GET_BOOKING.route("/get_booking/<id>", methods=["GET"])
def get_booking(id):
    try:

        db = firebase_service.db
        

        # Crear servicio en Firestore
        doc_ref = db.collection("reservas").where("businessId","==",id)
        doc_snapshot = doc_ref.stream()
        
        bookings = [{id:doc.id, **doc.to_dict()} for doc in doc_snapshot]

        if not bookings:
            return jsonify({"status": 404, "details": "No se encontraron las reservas"}), 404

        return jsonify({"status": 200, "details": bookings}), 200

    except Exception as e:
        print("error",str(e))
        return jsonify({"status": 500, "error": str(e)}), 500
