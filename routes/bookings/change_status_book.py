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
    payment_amount = data["paymentAmount"]
    price = data["price"]
    
    if payment_amount:
        payment_amount = price

    try:
        booking_ref = db.collection("reservas").where("id", "==", booking_id).get()
        booking_list = list(booking_ref)

        if not booking_list:
            return jsonify({"status": 404, "details": "Reserva no encontrada"}), 404

        for book in booking_list:
            update_data={
                "status":new_status
            }
            if payment_amount is None and price is not None:
                payment_amount = price

            book.reference.update(update_data)

        update_status = [
            {"id": book.id, **book.reference.get().to_dict()} for book in booking_list
        ]

        socketio.emit("update_status",{
            "action":"update",
            "updates":update_status
        })
        
        return jsonify({"status": 200, "details": update_status}), 200

    except Exception as e:
        return jsonify({
            "status": 500,
            "details": f"Error interno: {e}"
        }), 500
