from app.config import AppSettings

from pydantic import BaseModel, EmailStr
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from itsdangerous import URLSafeTimedSerializer

settings = AppSettings()

# Email config
config = ConnectionConfig(
    MAIL_USERNAME="alvaro@alvarogalvan.com",
    MAIL_PASSWORD="",
    MAIL_FROM="alvaro@alvarogalvan.com",
    MAIL_PORT=587,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_SSL_TLS=True,
    MAIL_FROM_NAME="Alvaro Galvan",
)

login_key = settings.login_key
serializer = URLSafeTimedSerializer(login_key)


class EmailSchema(BaseModel):
    email: EmailStr
