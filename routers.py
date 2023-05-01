from controllers import auth, posts, follow, users
from fastapi import APIRouter
router = APIRouter(prefix='/sm')

router.include_router(auth.router)
router.include_router(posts.router)
router.include_router(follow.router)
router.include_router(users.router)
