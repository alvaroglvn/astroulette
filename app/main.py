from fastapi import FastAPI
from app.dependencies import get_db
from app.routers.route_chars import *

app = FastAPI()
# Include routes
app.include_router("")
