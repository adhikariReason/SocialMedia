from fastapi import APIRouter, HTTPException
from datetime import datetime
from firebase_admin import db
from credentials.database import firebasedb

router = APIRouter()