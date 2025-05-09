FROM python:3.13.3-slim-bullseye

ENV COOKIE_DOMAIN=".fly.dev"
ENV FRONTEND_URL="https://astroulette.fly.dev"

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]