from flask import Flask
from flask_cors import CORS
import os
from dotenv import load_dotenv
from config.socket_config import socketio

# Blueprints
from routes.auth.users.register import SIGNUP_BP
from routes.auth.users.login import LOGIN_BP
from routes.auth.users.userData import GET_USER
from routes.auth.business.register_company import REGISTER_COMPANY
from routes.company.get_all_business import ALL_BUSINESS
from routes.company.get_business_id import GET_BUSINESS_ID
from routes.company.register_employee import CREATE_EMPLOYEE
from routes.company.all_employees import ALL_EMPLOYEE
from routes.company.schedules import SCHEDULES
from routes.company.get_schedules import GET_SCHEDULES
from routes.company.employee_status import EMPLOYEE_STATUS
from routes.company.delete_schedule import DELETE_SCHEDULE
from routes.company.business_hours import BUSINESS_HOURS
from routes.company.business_hours_delete import BUSINESS_HOURS_DELETE
from routes.company.get_business_hours import ALL_BUSINESS_HOURS
from routes.company.update_business_hours import UPDATE_BUSINESS_SCHEDULE 
from routes.company.delete_service import DELETE_SERVICE
from routes.company.get_services import GET_SERVICE
from routes.company.update_service_status import UPDATE_SERVICE_STATUS
from routes.company.create_service import CREATE_SERVICE
from routes.bookings.create_booking import CREATE_BOOKING
from routes.bookings.get_bookings import GET_BOOKING
from routes.bookings.user_booking import GET_USER_BOOKING
from routes.company.get_employee_byId import GET_EMPLOYEE_BY_ID
from routes.company.update_service_card import UPDATE_SERVICE_CARD
from routes.bookings.cancel_reservation import DELETE_BOOKING
from routes.company.delete_employee import DELETE_EMPLOYEE
from routes.mercado_pago.user_authorization import USER_AUTHORIZATION
from routes.mercado_pago.salesman_data import SALESMAN_DATA
from routes.mercado_pago.preferences import PREFERENCES_MP
from routes.mercado_pago.payment_webhook import PAYMENT_WEBHOOK
from routes.bookings.change_status_book import STATUS_BOOK
from routes.account_settings.company.settings_profile import SETTINGS_PROFILE
from routes.mercado_pago.delete_mp_auth import DELETE_MP_AUTH
from routes.bookings.get_all_bookings import GET_ALL_BOOKING
from routes.bookings.status_payment import STATUS_PAYMENT
from routes.mercado_pago.subscriptions import SUBSCRIPTIONS

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get("SUPER_SECRET_KEY")


# 🔐 CORS global
CORS(app, resources={r"/*": {"origins": "*"}})

# 🔌 SocketIO con Gevent
socketio.init_app(app, cors_allowed_origins="*", async_mode="gevent")

# 👂 Eventos de conexión/desconexión
@socketio.on("connect")
def handle_connect():
    print("🟢 WebSocket conectado",socketio)

@socketio.on("disconnect")
def handle_disconnect():
    print("🔴 WebSocket desconectado",socketio)

# 🧩 Rutas
app.register_blueprint(SIGNUP_BP)
app.register_blueprint(LOGIN_BP)
app.register_blueprint(GET_USER)
app.register_blueprint(REGISTER_COMPANY)
app.register_blueprint(ALL_BUSINESS)
app.register_blueprint(GET_BUSINESS_ID)
app.register_blueprint(CREATE_EMPLOYEE)
app.register_blueprint(ALL_EMPLOYEE)
app.register_blueprint(SCHEDULES)
app.register_blueprint(GET_SCHEDULES)
app.register_blueprint(EMPLOYEE_STATUS)
app.register_blueprint(DELETE_SCHEDULE)
app.register_blueprint(BUSINESS_HOURS)
app.register_blueprint(BUSINESS_HOURS_DELETE)
app.register_blueprint(ALL_BUSINESS_HOURS)
app.register_blueprint(DELETE_SERVICE)
app.register_blueprint(GET_SERVICE)
app.register_blueprint(UPDATE_SERVICE_STATUS)
app.register_blueprint(CREATE_SERVICE)
app.register_blueprint(UPDATE_BUSINESS_SCHEDULE)
app.register_blueprint(CREATE_BOOKING)
app.register_blueprint(GET_BOOKING)
app.register_blueprint(GET_USER_BOOKING)
app.register_blueprint(GET_EMPLOYEE_BY_ID)
app.register_blueprint(UPDATE_SERVICE_CARD)
app.register_blueprint(DELETE_BOOKING)
app.register_blueprint(DELETE_EMPLOYEE)
app.register_blueprint(USER_AUTHORIZATION)
app.register_blueprint(SALESMAN_DATA)
app.register_blueprint(PREFERENCES_MP)
app.register_blueprint(PAYMENT_WEBHOOK)
app.register_blueprint(STATUS_BOOK)
app.register_blueprint(SETTINGS_PROFILE)
app.register_blueprint(DELETE_MP_AUTH)
app.register_blueprint(GET_ALL_BOOKING)
app.register_blueprint(STATUS_PAYMENT)
app.register_blueprint(SUBSCRIPTIONS)



@app.route("/")
def home():
    return "Servidor Flask activo ✅"


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    socketio.run(app, host="0.0.0.0", port=port)




