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
RUN pip install --no-cache-dir --upgrade -r /api/requirements.txt
COPY . /api

# Install playwright
RUN playwright install chromium-headless-shell

# set environment variables
CMD ["fastapi", "run", "main.py", "--port", "8022"]
