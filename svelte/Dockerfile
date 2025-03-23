# Build the SvelteKit frontend
FROM node:22-slim AS build-frontend
WORKDIR /frontend
COPY . /frontend

# Declare build arguments
ARG REDIS_URL
ARG API_URL

# Set environment variables for build time
ENV REDIS_URL=${REDIS_URL}
ENV API_URL=${API_URL}

RUN npm install -g pnpm@10.6.5
RUN pnpm install
RUN pnpm run build

EXPOSE 4000

# Set runtime command with environment variables
CMD ["sh", "-c", "REDIS_URL=${REDIS_URL} API_URL=${API_URL} PORT=4000 node build"]
