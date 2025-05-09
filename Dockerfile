FROM python:3.13.3-slim-bullseye

# Install Node.js 18, Nginx, and Supervisor
RUN apt-get update && \
    apt-get install -y curl gnupg2 ca-certificates nginx supervisor && \
    curl -fsSL https://deb.nodesource.com/setup_18.x | bash - && \
    apt-get install -y nodejs && \
    apt-get clean

# Copy Python backend
ENV FRONTEND_URL="https://astroulette.fly.dev"
WORKDIR /app
COPY app/ .
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r ./requirements.txt

# Copy frontend and install/build
ENV PUBLIC_API_URL="/api"
WORKDIR /frontend-svltkit
COPY frontend-svltkit/ .
RUN npm install
RUN npm run build

# Return to root and copy configs
WORKDIR /
COPY supervisord.conf .
COPY nginx.conf /etc/nginx/nginx.conf

# Set exposed port (same as Nginx's listen port)
EXPOSE 3000

# Start all services
CMD ["supervisord", "-c", "supervisord.conf"]