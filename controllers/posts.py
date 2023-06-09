from fastapi import APIRouter, HTTPException
from datetime import datetime
from firebase_admin import db
from credentials.database import firebasedb
from controllers.auth import protected

db = firebasedb()
router = APIRouter(prefix="/posts")

# Define endpoint to create a new post
@router.post("/create")
async def create_post(content: str, username: str, visibility: str):
    # Generate a new unique ID for the post
    new_post_id = db.child('posts').push().key
    
    # Get the current datetime
    created_at = datetime.utcnow().isoformat()
    
    # Create a dictionary representing the new post
    new_post = {
        "content": content,
        "createdBy": username,
        "createdAt": str(datetime.now()),
		"visibility": visibility
    }
    
    # Save the new post to Firebase Realtime Database
    db.child(f"posts/{new_post_id}").set(new_post)
    post_created_ref = db.child(f"users/{username}/editAccess/ids")
    post_created_ids = post_created_ref.get()
    if post_created_ids is None:
        post_created_index = 0
    else:
        post_created_index = len(post_created_ids)
    post_created_ref.child(str(post_created_index)).set(new_post_id)

    # Return the new post ID
    return {"id": new_post_id}

@router.get("/get/all/")
async def get_all_posts(usernames: str):
	username_list = usernames.split(",")
	all_posts = []
	for username in username_list:
				posts1 = db.child('users').child(username).child("editAccess").child("ids").get()
				if not posts1 is None:
					posts = [db.child('posts').child(x).get() for x in posts1 if db.child(f"posts/{x}/visibility").get() == "public"]
					all_posts.extend(posts)
	if len(all_posts) == 0:
		raise HTTPException(status_code=404, detail="No post Available")
	return all_posts

@router.post("/change-visibility/")
async def change_visibility(username:str, postId: str, type: str):
	editAccessPosts = db.child('users').child(username).child("editAccess").child("ids").get()
	if not postId in editAccessPosts:
		raise HTTPException(status_code=404, detail="No edit permission")
	post = db.child('posts').child(postId).child("visibility").set(type)
	return "Done"


'''
# Needs filtration!!!
# Right Now: Gets all the data from all the people that are followed by the user,
	Sort them date wise with latest first and display to the user.
	Only looks for visibility of private. Need to introduce the listed as well.
# Future Plan: Only get recommended data from the database. Check for visibility as well.
'''
@router.get("/get/timeline")
async def get_timeline(username: str, offset: int):
	follows = db.child(f"users/{username}/followed/ids").get()
	followed_users = list(follows.keys())
	all_posts = await (get_all_posts(','.join(followed_users)))

	all_posts.sort(key=lambda x: x['createdAt'], reverse=True)
	return all_posts


