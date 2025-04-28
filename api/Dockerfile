# Stage 1: Build the FastAPI backend
FROM python:3.11-slim as requirements-stage
WORKDIR /tmp
RUN pip install poetry
RUN poetry self add poetry-plugin-export
COPY ./pyproject.toml ./poetry.lock* /tmp/
RUN poetry export --output requirements.txt --without-hashes

# Stage 2: Serve the FastAPI backend
FROM python:3.11-slim
WORKDIR /api
COPY --from=requirements-stage /tmp/requirements.txt /api/requirements.txt

# Install system dependencies required by Playwright
RUN apt-get update && apt-get install -y \
    libglib2.0-0 \
    libnss3 \
    libnspr4 \
    libdbus-1-3 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libdrm2 \
    libxkbcommon0 \
    libxcomposite1 \
    libxdamage1 \
    libxfixes3 \
    libxrandr2 \
    libgbm1 \
    libasound2 \
    libpango-1.0-0 \
    libcairo2 \
    libatspi2.0-0 \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir --upgrade -r /api/requirements.txt
COPY . /api

# Install playwright
RUN playwright install chromium-headless-shell

# set environment variables
CMD ["fastapi", "run", "main.py", "--port", "8022"]
