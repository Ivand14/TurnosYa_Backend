import os
from flask import Blueprint, jsonify, request
from dotenv import load_dotenv
from config.firebase_service import db
import requests
from google.cloud.firestore import DELETE_FIELD

load_dotenv()

ACCESS_TOKEN = os.getenv("MP_ACCESS_TOKEN_PROD")

SUBSCRIPTIONS = Blueprint("SUBSCRIPTIONS", __name__)


@SUBSCRIPTIONS.route("/subscribe", methods=["POST"])
def subscribe():
    data = request.get_json()
    if not data or "email" not in data or "amount" not in data:
        return jsonify({"error": "Invalid request data"}), 400

    # Validate email format
    if "@" not in data["email"] or "." not in data["email"]:
        return jsonify({"error": "Invalid email format"}), 400

    # Validate amount
    try:
        amount = float(data["amount"])
        if amount <= 0:
            raise ValueError("Amount must be greater than zero")
    except (ValueError, TypeError):
        return jsonify({"error": "Invalid amount"}), 400



    payload = {
        "reason": data.get("reason", "Suscripción mensual"),
        "auto_recurring": {
            "frequency": 1,
            "frequency_type": "months",
            "billing_day": 5,
            "billing_day_proportional": False,
            "transaction_amount": amount,
            "currency_id": "ARS",
            "free_trial": {
                "frequency": data.get("free_trial", 7),
                "frequency_type": "days"
            }
        },
        "payment_methods_allowed": {
            "payment_types": [
                {"id": "credit_card"},
                {"id": "debit_card"},
                {"id": "account_money"}
            ]
        },
        "back_url": "https://www.uturns.lat/register-business"
    }

    try:
        response = requests.post(
        "https://api.mercadopago.com/preapproval",
        headers={"Authorization": f"Bearer {ACCESS_TOKEN}"},
        json=payload
        )

        response_data = response.json()

        return jsonify({
            "init_point": response_data.get("init_point"),
            "preapproval_id": response_data.get("id"),
            "status": 200
        })
    except requests.RequestException as e:
        return jsonify({"error": "Failed to create subscription", "details": str(e)}), 500
    except Exception as e:
        return jsonify({"error": "Failed to create subscription", "details": str(e)}), 500


@SUBSCRIPTIONS.route("/plan/cancel/<preapproval_id>", methods=["PUT"])
def cancel_subscription(preapproval_id):
    if not preapproval_id:
        return jsonify({"error": "preapproval_id is required"}), 400

    try:
        response = requests.put(
        f"https://api.mercadopago.com/preapproval/{preapproval_id}",
        headers={"Authorization": f"Bearer {ACCESS_TOKEN}"},
        json={"status": "cancelled"}
        )

        if response.status_code != 200:
            return jsonify({"error": "Failed to cancel subscription"}), response.status_code

        business_subscriptions = db.collection("empresas").where("mercado_pago_subscription.id", "==", preapproval_id).get()

        for subscription in business_subscriptions:
            subscription.reference.update({
                "mercado_pago_subscription": DELETE_FIELD,
                "preapproval_id": DELETE_FIELD,
                "subscriptionPlan": DELETE_FIELD
            })

        return jsonify({
            "message": "Subscription cancelled successfully",
            "status": 200
        })
    except requests.RequestException as e:
        return jsonify({"error": "Failed to cancel subscription", "details": str(e)}), 500
    except Exception as e:
        return jsonify({"error": "Failed to cancel subscription", "details": str(e)}), 500


@SUBSCRIPTIONS.route("/plan/information/<preapproval_id>", methods=["GET"])
def get_plan_information(preapproval_id):
    try:
        if not preapproval_id:
            return jsonify({"error": "preapproval_id is required"}), 400

        response = requests.get(
            f"https://api.mercadopago.com/preapproval/{preapproval_id}",
            headers={"Authorization": f"Bearer {ACCESS_TOKEN}"}
        )

        if response.status_code != 200:
            return jsonify({"error": "Failed to retrieve plan information"}), response.status_code

        plan_info = response.json()
        return jsonify({
            "plan_info": plan_info,
            "status": 200
        })
    except requests.RequestException as e:
        return jsonify({"error": "Failed to retrieve plan information", "details": str(e)}), 500
    except Exception as e:
        return jsonify({"error": "Failed to retrieve plan information", "details": str(e)}), 500