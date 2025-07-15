from flask import Blueprint, jsonify,request
from config import firebase_service
from config.socket_config import socketio

STATUS_BOOK = Blueprint("STATUS_BOOK", __name__)

@STATUS_BOOK.route("/status_book", methods=["PATCH"])
def status_book():
    db = firebase_service.db
    data = request.get_json()

    if not data or "booking_id" not in data or "new_status" not in data:
        return jsonify({"status": 400, "details": "Faltan datos requeridos"}), 400

    booking_id = data["booking_id"]
    new_status = data["new_status"]

    try:
        booking_ref = db.collection("reservas").document(booking_id).get()

        if not booking_ref.exists:
            return jsonify({"status": 404, "details": "Reserva no encontrada"}), 404

        booking_ref.reference.update({"status": new_status})

        update_status = {"id": booking_ref.id, **booking_ref.to_dict()}
        socketio.emit("update_status_book", update_status)

        return jsonify({"status": 200, "details": update_status}), 200

    except Exception as e:
        return jsonify({"status": 500, "details": f"Error interno: {e}"}), 500

    