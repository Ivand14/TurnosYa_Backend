import firebase_admin
from firebase_admin import credentials, firestore
import json
import threading

db = None  

def initialize_firebase():
    global db
    try:
        secret_path = "/etc/secrets/turnos_ya.json"
        with open(secret_path) as f:
            firebase_config = json.load(f)

        cred = credentials.Certificate(firebase_config)
        firebase_admin.initialize_app(cred, {
            "storageBucket": "turnosya-c5672.firebasestorage.app"
        })
        db = firestore.client()
        print("✅ Firebase SDK inicializado correctamente.")
    except Exception as e:
        print("❌ Error al inicializar Firebase:", e)


firebase_thread = threading.Thread(target=initialize_firebase)
firebase_thread.start()
