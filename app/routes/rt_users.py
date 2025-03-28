from fastapi import APIRouter
from fastapi.responses import JSONResponse

from app.dependencies import *
from app.models import MagicLinkRequest
from app.services.mailer import send_magic_link, create_token
from app.db.db_crud import create_record, read_one_by_field
from app.db.db_models import User


router = APIRouter()


@router.post("/user")
async def register_or_login(
    payload: MagicLinkRequest,
    session: db_dependency,
    settings: settings_dependency,
) -> JSONResponse:
    try:
        user_email: EmailStr
        # Load the user
        user = await read_one_by_field(session, User, "email", payload.email)

        if user:
            user_email = user.email
        # If no user exists, create and store it
        else:
            token, expiry = create_token()
            new_user = User(
                username=payload.username,
                email=payload.email,
                active=True,
                login_token=token,
                token_expiry=expiry,
            )
            # Store new user
            stored_user = await create_record(session, new_user)
            user_email = stored_user.email

        await send_magic_link(
            settings,
            user_email,
        )

    except Exception as e:
        return JSONResponse(content=f"Unexpected error: {e}", status_code=500)
