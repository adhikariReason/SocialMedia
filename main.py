from fastapi import FastAPI, APIRouter
import routers

app = FastAPI()

# Mount controllers
app.include_router(routers.router)

