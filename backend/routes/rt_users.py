import time
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from backend.config.settings import settings_dependency
from backend.config.session import db_dependency
from backend.schemas import MagicLinkRequest, UserPatchData
from backend.services.mailer import send_magic_link
from backend.services.auth import (
    create_mailer_token,
    create_access_token,
    admin_only_dependency,
    valid_user_dependency,
)
from backend.db.db_crud import (
    create_record,
    read_record,
    read_one_by_field,
    read_all,
    update_record,
)
from backend.db.db_models import User
from backend.db.db_excepts import DatabaseError, TableNotFound, RecordNotFound

router = APIRouter()


@router.post("/user/login")
async def register_or_login(
    payload: MagicLinkRequest,
    session: db_dependency,
    settings: settings_dependency,
) -> JSONResponse:
    try:
        try:
            user = await read_one_by_field(session, User, "email", payload.email)
        except RecordNotFound:
            user = None

        # If no user exists, create and store it
        if not user:
            token, expiry = create_mailer_token()
            new_user = User(
                username=payload.username,
                email=payload.email,
                status="active",
                role="user",
                login_token=token,
                token_expiry=expiry,
            )
            user = await create_record(session, new_user)
            if not user:
                raise HTTPException(status_code=500, detail="Failed to storenew user.")
            await send_magic_link(settings, user.email, token)
            return JSONResponse(
                content=f"User {user.username} registered", status_code=201
            )
        else:
            token, expiry = create_mailer_token()
            user.login_token = token
            user.token_expiry = expiry
            await session.commit()
            await send_magic_link(settings, user.email, token)
            return JSONResponse(
                content=f"Login link sent to {user.email}", status_code=200
            )

    except Exception as e:
        return JSONResponse(content=f"Unexpected error: {e}", status_code=500)


@router.get("/user/verify")
async def verify_magic_link(
    token: str, session: db_dependency, settings: settings_dependency
) -> JSONResponse:
    user = await read_one_by_field(session, User, "login_token", token)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token.")

    if user.token_expiry < int(time.time()):
        raise HTTPException(status_code=401, detail="Token is expired.")

    access_token = create_access_token(
        data={"sub": str(user.id)},
        secret_key=settings.secret_key,
        expires_in_seconds=60 * 60 * 24 * 7,
    )

    response = JSONResponse({"message": "Login verified"})
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=True,
        samesite="none",
        max_age=60 * 60 * 24 * 7,
        path="/",
    )
    return response


@router.get("/user/me")
async def get_current_user(user: valid_user_dependency) -> JSONResponse:
    return JSONResponse(
        content={
            "id": user.id,
            "username": user.username,
            "email": user.email,
        },
        status_code=200,
    )


@router.get("/user/logout")
async def logout_user() -> JSONResponse:
    response = JSONResponse(content={"message": "Logged out"}, status_code=200)
    response.delete_cookie(key="access_token", path="/")
    return response


@router.post("/user")
async def add_user(
    user: User,
    session: db_dependency,
    admin: admin_only_dependency,
) -> JSONResponse:
    try:
        new_user = User(
            username=user.username,
            email=user.email,
            status=user.status,
            role=user.role,
            login_token="None",
            token_expiry=0,
        )
        stored_user = await create_record(session, new_user)
        if not stored_user:
            raise HTTPException(status_code=500, detail="Failed to store new user.")
        return JSONResponse(
            content=f"User {stored_user.username} created.", status_code=201
        )
    except Exception as e:
        return JSONResponse(content=f"Unexpected error: {e}", status_code=500)


@router.get("/user")
async def get_all_users(session: db_dependency) -> JSONResponse:
    try:
        users = await read_all(session, User)
        if not users:
            return JSONResponse(content="No users found.", status_code=404)
        result = {"user": [user.model_dump() for user in users]}
        return JSONResponse(content=result, status_code=200)
    except (DatabaseError, TableNotFound) as e:
        return JSONResponse(content=e.detail, status_code=e.status_code)
    except Exception as e:
        return JSONResponse(content=f"Unexpected error: {e}", status_code=500)


@router.get("/user/{user_id}")
async def get_user(session: db_dependency, user_id: int) -> JSONResponse:
    try:
        user = await read_record(session, User, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found.")
        return JSONResponse(content=user.model_dump(), status_code=200)
    except (DatabaseError, RecordNotFound, TableNotFound) as e:
        return JSONResponse(content=e.detail, status_code=e.status_code)
    except Exception:
        return JSONResponse(content="Unexpected error", status_code=500)


@router.patch("/user/{user_id}")
async def update_user(
    user_id: int,
    session: db_dependency,
    updates: UserPatchData,
    admin: admin_only_dependency,
) -> JSONResponse:
    try:
        updated_user = await update_record(
            session, User, user_id, updates.model_dump(exclude_unset=True)
        )

        return JSONResponse(content=updated_user, status_code=200)
    except (DatabaseError, RecordNotFound, TableNotFound) as e:
        return JSONResponse(content=e.detail, status_code=e.status_code)
    except Exception:
        return JSONResponse(content="Unexpected error", status_code=500)


@router.delete("user/{user_id}")
async def delete_user(
    session: db_dependency, user_id: int, admin: admin_only_dependency
) -> JSONResponse:
    try:
        await update_record(session, User, user_id, {"status": "deleted"})
        return JSONResponse(content="User deleted", status_code=200)
    except (DatabaseError, RecordNotFound, TableNotFound) as e:
        return JSONResponse(content=e.detail, status_code=e.status_code)
    except Exception:
        return JSONResponse(content="Unexpected error", status_code=500)
