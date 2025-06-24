import firebase_admin
from firebase_admin import credentials, firestore
import json
import traceback

db = None

def initialize_firebase():
    global db
    try:
        if not firebase_admin._apps:
            with open("/etc/secrets/turnos_ya.json") as f:
                firebase_config = json.load(f)
            cred = credentials.Certificate(firebase_config)
            firebase_admin.initialize_app(cred, {
                "storageBucket": "turnosya-c5672.firebasestorage.app"
            })
            db = firestore.client()
            print("✅ Firebase SDK inicializado correctamente.")
    except Exception as e:
        print("❌ Error al inicializar Firebase:", e)
        print(traceback.format_exc())

initialize_firebase()
