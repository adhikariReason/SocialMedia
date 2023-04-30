from fastapi import APIRouter, HTTPException
from datetime import datetime
from firebase_admin import db
from credentials.database import firebasedb

db = firebasedb()
router = APIRouter(prefix="/follow")

@router.post("/follow-user/")
async def followUser(followUsername: str, username: str):
	userCheck = db.child(f"users/{followUsername}").get()
	if userCheck is None:
		raise HTTPException(status_code = 404, detail = f"User {followUsername} Doesn't Exist")
	db.child(f"users/{username}/followed/ids").update({followUsername:True})
	return f"{username} followed {followUsername}"