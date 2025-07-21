from flask import Blueprint, jsonify, request
from config import firebase_service
from config.socket_config import socketio

STATUS_PAYMENT = Blueprint("STATUS_PAYMENT", __name__)

@STATUS_PAYMENT.route("/status_payment", methods=["PATCH"])
def status_book():
    db = firebase_service.db
    data = request.get_json()

    # Validar campos necesarios
    if not all(key in data for key in ("bookingId", "status", "payment_id", "payment_status")):
        return jsonify({"status": 400, "details": "Faltan datos requeridos"}), 400

    payment_id = data["payment_id"]
    payment_status = data["payment_status"]
    bookingId = data["bookingId"]
    status = data["status"]

    try:
        # Buscar la reserva por ID (campo "id" en Firestore, no ID del documento)
        booking_ref = db.collection("reservas").where("id", "==", bookingId).get()
        booking_list = list(booking_ref)

        if not booking_list:
            return jsonify({"status": 404, "details": "Reserva no encontrada"}), 404

        update_status = []

        for book in booking_list:
            book.reference.update({
                "paymentStatus": payment_status,
                "payment_id": payment_id,
                "status": status
            })
            # Obtener datos actualizados
            updated_data = book.reference.get().to_dict()
            update_status.append({"id": book.id, **updated_data})

        # Emitir evento por socket
        socketio.emit("update_payment", {
            "action": "update",
            "updates": update_status
        })

        return jsonify({"status": 200, "details": update_status}), 200

    except Exception as e:
        return jsonify({
            "status": 500,
            "details": f"Error interno: {str(e)}"
        }), 500
