# Build the SvelteKit frontend
ARG REDIS_URL
FROM node:22-slim AS build-frontend
WORKDIR /frontend
COPY . /frontend
RUN npm install -g pnpm@10.6.5
RUN pnpm install
# ENV REDIS_URL=${REDIS_URL}
RUN pnpm run build
EXPOSE 8000
ENV API_URL=http://localhost:8000
CMD ["API_URL=http://localhost:8000", "REDIS_URL=${REDIS_URL}", "PORT=4000", "node", "build"]
