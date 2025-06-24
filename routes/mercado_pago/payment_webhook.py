from flask import Blueprint,jsonify,request
import requests
import os

PAYMENT_WEBHOOK = Blueprint("PAYMENT_WEBHOOK",__name__)

@PAYMENT_WEBHOOK.route("/payment",methods=["POST"])
def payment_webhook():
    data = request.json

    if not data:
        return jsonify({'error': 'No data received'}), 400

    payment_id = data.get('data', {}).get('id')
    if not payment_id:
        return jsonify({'error': 'No payment ID'}), 400

    mp_response = requests.get(
        f'https://api.mercadopago.com/v1/payments/{payment_id}',
        headers={
            'Authorization': f'Bearer {os.getenv("MP_ACCESS_TOKEN_PROD")}' 
        }
    )

    if mp_response.status_code == 200:
        payment_info = mp_response.json()
        print(f"Estado del pago: {payment_info.get('status')}")
        return jsonify({'status': payment_info.get('status')}), 200
    else:
        return jsonify({'error': 'No se pudo consultar el estado del pago'}), 500