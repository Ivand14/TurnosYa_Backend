from flask import Blueprint, jsonify,request
from config import firebase_service
from config.socket_config import socketio
from firebase_admin import storage

SETTINGS_PROFILE = Blueprint("SETTINGS_PROFILE", __name__)

@SETTINGS_PROFILE.route("/config/profile",methods=["PATCH"])
def setting_profile():
    db = firebase_service.db
    data = request.get_json()

    
    if not "businessId" in data :
        return jsonify({"status": 400, "details": "Faltan datos requeridos"}), 400

    name = data.get("name")
    email = data.get("email")
    phone = data.get("phone")
    address = data.get("address")
    description = data.get("description")
    business_id = data.get("businessId")
    logo = data.get("logo")
    
    update_data = {}

    # Solo actualizamos si hay valor
    if name:
        update_data["company_name"] = name
    if email:
        update_data["email"] = email
    if phone:
        update_data["phone"] = phone
    if address:
        update_data["address"] = address
    if description:
        update_data["description"] = description
    if logo:
        update_data["logo"] = logo

    if not update_data:
        return jsonify({"status": 400, "details": "No hay datos para actualizar"}), 400
    
    try:
        
        profile_doc = db.collection("empresas").where("id","==",business_id).get()
        
        profile_list = list(profile_doc)
        
        for prof in profile_list:
            prof.reference.update(update_data)
        
        update_profile = [{"id":prof.id,**prof.reference.get().to_dict()} for prof in profile_list]
        
        socketio.emit("update_profile",{
            "action":"update",
            "profile":update_profile
        })
        
        return jsonify({"status": 200, "details": update_profile}), 200
        
    except Exception as e:
        return jsonify({
            "status": 500,
            "details": f"Error interno: {e}"
        }), 500