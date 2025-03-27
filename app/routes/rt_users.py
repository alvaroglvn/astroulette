from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter()


@router.post("/user")
async def register_user():
    pass
