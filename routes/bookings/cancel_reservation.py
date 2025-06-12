from flask import Blueprint, jsonify, request
from config import firebase_service
from config.socket_config import socketio
DELETE_BOOKING = Blueprint("DELETE_BOOKING", __name__)

@DELETE_BOOKING.route("/cancel_booking/<bookingId>", methods=["DELETE"])
def cancel_booking(bookingId):
    db = firebase_service.db
    try:

        if not bookingId:
            return jsonify({"status": 400, "details": "ID requerido"}), 400
        
        doc_ref = db.collection("reservas").where("id", "==", bookingId)
        doc_snap = doc_ref.stream()
        doc_list= list(doc_snap)

        if not doc_list:
            return jsonify({"status": 404, "details": "Reserva no encontrada"}), 404

        for doc in doc_list:
            doc.reference.delete()
            
        socketio.emit(
            "new_book",
            {
                "action":"cancel",
                "reserva":bookingId
            },
        )

        return jsonify({"status": 200, "details": f"Reserva eliminada: {bookingId}"}), 200

    except Exception as e:
        print("error",str(e))
        return jsonify({"status": 500, "error": str(e)}), 500
