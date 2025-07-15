from flask import Blueprint, jsonify,request
from config import firebase_service
from config.socket_config import socketio

STATUS_BOOK = Blueprint("ALL_EMPLOYEE", __name__)

@STATUS_BOOK.route("/status_book", methods=["PATCH"])
def status_book():
    db = firebase_service.db
    data = request.json()
    booking_id = data["booking_id"]
    new_status = data["new_status"]
    
    try:
        booking_ref = db.collection("reservas").where("id","==",booking_id).get()
        
        booking_list = list(booking_ref)
        
        if not booking_list:
            return jsonify({"status": 404, "details": "reserva no encontrada"}), 404
         
        for book in booking_list:
            book.reference.update({
                "status":new_status
            })
             
        update_status = [
            {"id":doc.id,**doc.reference.get().to_dict()} for doc in booking_list
        ]

        
        socketio.emit("update_status_book",update_status)
        
        return jsonify({"status": 200, "details": update_status}), 200
        
    except Exception as e:
        return jsonify({
            "status": 500,  
            "details": f"Error {e}",
        })
    
    