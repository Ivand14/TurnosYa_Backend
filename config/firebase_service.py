import firebase_admin
from firebase_admin import credentials,firestore

import json
import os

with open(os.path.join(os.path.dirname(__file__), "turnos_ya.json")) as f:
    firebase_config = json.load(f)

def initialize_firebase():
    cred = credentials.Certificate(
            firebase_config
    )
    firebase_admin.initialize_app(cred,{
        "storageBucket": "turnosya-c5672.firebasestorage.app"
    })
    print("Firebase SDK inicializado correctamente.")
    return firestore.client()

db = initialize_firebase()
    