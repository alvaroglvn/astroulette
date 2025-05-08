# -------------------------------------
# STAGE 1: Build
# -------------------------------------
FROM node:24-alpine AS builder

WORKDIR /app

# Install dependencies
COPY package.json package-lock.json ./
RUN npm install

# Copy source code
COPY . .

# Inject public env var (for build-time use)
ENV PUBLIC_API_URL="https://mars-roulette.fly.dev"

# Build app
RUN npm run build

# -------------------------------------
# STAGE 2: Serve with Node adapter
# -------------------------------------
FROM node:24-alpine

WORKDIR /app

COPY --from=builder /app/build ./build
COPY --from=builder /app/package.json ./
COPY --from=builder /app/.svelte-kit ./.svelte-kit
COPY --from=builder /app/node_modules ./node_modules

# Install production dependencies (if any are needed for serving)
RUN npm install --omit=dev

# Expose the default port
EXPOSE 3000

# Start app (uses Node adapter)
CMD ["node", "build"]