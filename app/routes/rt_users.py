from fastapi import APIRouter
from fastapi.responses import JSONResponse

from app.dependencies import *
from app.models import MagicLinkRequest, UserPatchData
from app.services.mailer import send_magic_link, create_token
from app.db.db_crud import create_record, read_record, read_one_by_field, read_all, update_record
from app.db.db_models import User
from app.db.db_excepts import *


router = APIRouter()


@router.post("/user/login")
async def register_or_login(
    payload: MagicLinkRequest,
    session: db_dependency,
    settings: settings_dependency,
) -> JSONResponse:
    try:
        user = await read_one_by_field(session, User, "email", payload.email)

        # If no user exists, create and store it
        if not user:
            token, expiry = create_token()
            new_user = User(
                username=payload.username,
                email=payload.email,
                active=True,
                login_token=token,
                token_expiry=expiry,
            )
            # Store new user
            user = await create_record(session, new_user)

        await send_magic_link(
            settings,
            user.email,
        )

        return JSONResponse(content=f"User {user.username} registered", status_code=200)

    except Exception as e:
        return JSONResponse(content=f"Unexpected error: {e}", status_code=500)


@router.post("/user")
async def add_user(
    user: User,
    session: db_dependency,
) -> JSONResponse:
    try:
        new_user = User(
            username=user.username,
            email=user.email,
            active=user.active,
            login_token=None,
            token_expiry=None,
        )
        stored_user = await create_record(session, new_user)
        return JSONResponse(
            content=f"User {stored_user.username} created.", status_code=201
        )
    except Exception as e:
        return JSONResponse(content=f"Unexpected error: {e}", status_code=500)


@router.get("/user")
async def get_all_users(session: db_dependency) -> JSONResponse:
    try:
        users = await read_all(session, User)
        result = {"user": [user.model_dump() for user in users]}
        return JSONResponse(content=result.model_dump(),
                            status_code=200)
    except (DatabaseError, TableNotFound) as e:
        return JSONResponse(content=e.detail, status_code=e.status_code)
    except Exception as e:
        return JSONResponse(content=f"Unexpected error: {e}", status_code=500)


@router.get("/user/{user_id}")
async def get_user(session: db_dependency, user_id:int) -> JSONResponse:
    try:
        user = await read_record(session, User, user_id)
        return JSONResponse(content=user.model_dump(),
                            status_code=200)
    except (DatabaseError, RecordNotFound, TableNotFound) as e:
        return JSONResponse(content=e.detail, status_code=e.status_code)
    except Exception as e:
        return JSONResponse(content="Unexpected error", status_code=500)

@router.patch("/user/{user_id}")
async def update_user(
    user_id: int,
    session: db_dependency,
    updates: UserPatchData,
) -> JSONResponse:
    try:
        updated_user = await update_record(
            session, User, user_id, updates.model_dump(exclude_unset=True)
        )

        return JSONResponse(content=updated_user.model_dump(), status_code=200)
    except (DatabaseError, RecordNotFound, TableNotFound) as e:
        return JSONResponse(content=e.detail, status_code=e.status_code)
    except Exception as e:
        return JSONResponse(content="Unexpected error", status_code=500)

@router.delete("user/{user_id}")
async def delete_user(session:db_dependency, user_id:int) -> JSONResponse:
    try:
        await inactive_user = await update_record(session, User, user_id, {"status":"deleted"})
    except (DatabaseError, RecordNotFound, TableNotFound) as e:
        return JSONResponse(content=e.detail, status_code=e.status_code)
    except Exception as e:
        return JSONResponse(content="Unexpected error", status_code=500)
    