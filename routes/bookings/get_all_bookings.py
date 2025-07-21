from flask import Blueprint, jsonify, request
from config import firebase_service

GET_ALL_BOOKING = Blueprint("GET_ALL_BOOKING", __name__)

@GET_ALL_BOOKING.route("/all_booking", methods=["GET"])
def get_booking():
    try:
        db = firebase_service.db
        doc_ref = db.collection("reservas")
        doc_snapshot = doc_ref.stream()

        bookings = [{"id": doc.id, **doc.to_dict()} for doc in doc_snapshot]

        if not bookings:
            return jsonify({
                "status": 404,
                "details": "No se encontraron las reservas"
            }), 404

        return jsonify({
            "status": 200,
            "details": bookings
        }), 200

    except Exception as e:
        print("🔥 Error al obtener reservas:", str(e))
        return jsonify({
            "status": 500,
            "error": str(e)
        }), 500

