# Stage 1: Build the FastAPI backend
FROM python:3.11-slim as requirements-stage
WORKDIR /tmp
RUN pip install poetry
COPY ./pyproject.toml ./poetry.lock* /tmp/
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

# Stage 2: Serve the FastAPI backend
FROM python:3.11-slim
WORKDIR /api
COPY --from=requirements-stage /tmp/requirements.txt /api/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /api/requirements.txt
COPY . /api
# set environment variables
CMD ["fastapi", "run", "main.py"]