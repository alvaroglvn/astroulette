import httpx
from pydantic import EmailStr
from app.config.settings import settings_dependency


async def send_magic_link(
    settings: settings_dependency,
    to: EmailStr,
    token: str,
) -> None:
    magic_link = f"https://marsroulette.com/login?token={token}"
    subject = "Your MarsRoulette Login"
    text = f"Click here to login: {magic_link}"

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"https://api.mailgun.net/v3/{settings.mailgun_domain}/messages",
                auth=("api", settings.mailgun_api_key),
                data={
                    "from": settings.from_email,
                    "to": to,
                    "subject": subject,
                    "text": text,
                },
            )
            response.raise_for_status()
        except Exception as e:
            raise Exception(f"Failed to send magic link: {e}")
