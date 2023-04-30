from fastapi import APIRouter, HTTPException
from fastapi.security import HTTPBasicCredentials
import jwt
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
import bcrypt
from firebase_admin import db
from credentials.database import firebasedb

db = firebasedb()
router = APIRouter()

load_dotenv() 
SECRET_KEY = os.environ.get('SECRET_KEY')
# HASH_SECRET = os.environ.get('HASH_SECRET').encode()
# Generate a random secret key for use with bcrypt
HASH_SECRET = bcrypt.gensalt()
print(HASH_SECRET, "chch")

def generate_token(username: str) -> str:
    payload = {
        'username': username,
        'exp': datetime.utcnow() + timedelta(minutes=60)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return token

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode(), hashed_password.encode())

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), HASH_SECRET).decode()

def verify_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        # Token has expired
        return {'error': 'Token has expired'}
    except jwt.InvalidTokenError:
        # Invalid token
        return {'error': 'Invalid token'}


@router.post("/login")
async def login(credentials: HTTPBasicCredentials):
    username = credentials.username
    password = credentials.password

    # Get user from Firebase Realtime Database
    user_ref = db.child('users').child(username)
    user = user_ref.get()
    print(user)
    if user is None or not verify_password(password, user["password"]):
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    token = generate_token(username)
    return {"access_token": token}


@router.get("/protected")
async def protected(token: str):
    payload = verify_token(token)
    if "error" in payload:
        raise HTTPException(status_code=401, detail=payload["error"])

    # If we get here, the token is valid and we can proceed with the protected action
    return {"username":payload["username"]}

@router.post("/signup")
async def signup(username: str, password: str):
    user_ref = db.child('users').child(username)
    if user_ref.get() is not None:
        raise HTTPException(status_code=400, detail="Username already exists")

    # Hash the password and add the new user to Firebase
    hashed_password = hash_password(password)
    user_ref.set({"password": hashed_password})

    # Generate a token for the new user
    token = generate_token(username)
    return {"access_token": token}