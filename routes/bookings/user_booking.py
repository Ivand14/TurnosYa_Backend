from flask import Blueprint, jsonify, request
from config import firebase_service

GET_USER_BOOKING = Blueprint("GET_USER_BOOKING", __name__)

@GET_USER_BOOKING.route("/user_booking/<id>", methods=["GET"])
def user_booking(id):
    try:

        db = firebase_service.db
        

        # Crear servicio en Firestore
        doc_ref = db.collection("reservas").where("userId","==",id)
        doc_snapshot = doc_ref.stream()
        
        bookings = [{id:doc.id, **doc.to_dict()} for doc in doc_snapshot]

        if not bookings:
            return jsonify({"status": 404, "details": "No se encontro la reserva"}), 404

        return jsonify({"status": 200, "details": bookings}), 200

    except Exception as e:
        print("error",str(e))
        return jsonify({"status": 500, "error": str(e)}), 500
