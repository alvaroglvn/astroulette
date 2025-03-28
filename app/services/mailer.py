import httpx
import uuid
import time
from pydantic import EmailStr
from fastapi.responses import JSONResponse
from app.config import AppSettings


async def send_magic_link(mail_settings: AppSettings, to: EmailStr, token: str) -> None:
    magic_link = f"https://marsroulette.com/login?token={token}"
    subject = "Your MarsRoulette Login"
    text = f"Click here to login: {magic_link}"

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"https://api.mailgun.net/v3/{mail_settings.mailgun_domain}/messages",
                auth=("api", mail_settings.mailgun_api_key),
                data={
                    "from": mail_settings.from_email,
                    "to": to,
                    "subject": subject,
                    "text": text,
                },
            )
            response.raise_for_status()
        except Exception as e:
            raise Exception(f"Failed to send magic link: {e}")


def create_token() -> tuple[str, int]:
    token = str(uuid.uuid4())
    expiry = int(time.time()) + 600  # ten minutes

    return token, expiry
