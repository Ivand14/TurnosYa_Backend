from flask import Blueprint, jsonify, request
from config import firebase_service
from config.socket_config import socketio

CREATE_BOOKING = Blueprint("CREATE_BOOKING", __name__)

@CREATE_BOOKING.route("/create_booking", methods=["POST"])
def create_booking():
    try:
        data = request.json
        db = firebase_service.db
        
        # Crear servicio en Firestore
        doc_ref = db.collection("reservas").add({
            "id": data["id"],
            "businessId": data["businessId"],
            "serviceName": data["serviceName"],
            "serviceId": data["serviceId"],
            "userId": data["userId"],
            "userName": data["userName"],
            "userEmail": data["userEmail"],
            "userPhone": data["userPhone"],
            "date": data["date"],
            "start": data["start"],
            "end": data["end"],
            "status": data["status"],
            "paymentStatus": data["paymentStatus"],
            "notes": data["notes"],
            "payment_id":data["payment_id"],
            "price": data["price"],
            "requiresDeposit": data["requiresDeposit"],
            "paymentPercentage": data["paymentPercentage"],
            "paymentAmount": data["paymentAmount"],
        })

        if not doc_ref:
            return jsonify({"status": 404, "details": "No se pudo crear la reserva"}), 404

        # Emitir evento WebSocket con los datos de la reserva
        socketio.emit("new_book", {
            "action": "crear",
            "reserva": data
        })

        return jsonify({"status": 200, "details": f"Reserva creada: {data}"}), 200

    except Exception as e:
        print("error", str(e))
        return jsonify({"status": 500, "error": str(e)}), 500
