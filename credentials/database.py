import firebase_admin
from firebase_admin import credentials, db

# Initialize Firebase app
cred = credentials.Certificate("credentials/socialmedia-f11a7-firebase-adminsdk-rnzba-d5ea840bf1.json")

firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://socialmedia-f11a7-default-rtdb.firebaseio.com/'
})

# Get a reference to the Firebase Realtime Database
db_ref = db.reference('/')

def firebasedb():
    return db_ref
