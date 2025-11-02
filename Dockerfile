# Stage 1: Build stage
FROM python:3.12-slim-bookworm AS builder

# Install uv
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Set the working directory
WORKDIR /app

# Copy your project files and lock file
# COPY requirements.txt .
# If using a pyproject.toml and uv lock, copy those instead
COPY pyproject.toml uv.lock ./

# Install dependencies using uv
RUN uv sync --frozen

# Stage 2: Runtime stage
FROM python:3.12-slim-bookworm

# Set the working directory
WORKDIR /app

# Copy the installed dependencies from the builder stage
COPY --from=builder /bin/uv /bin/uvx /bin/
# (above) Optional, if uv is needed at runtime
COPY --from=builder /app/.venv /app/.venv 
# (above) Copy the virtual environment

# Add the virtual environment to PATH
ENV PATH="/app/.venv/bin:${PATH}"

# Copy your application code
COPY main.py api_runner.py api/ models/ schemas/ setting/ static_data/ utilities/ ./

# Define the command to run your application
CMD ["uv", "run", "main.py", "--dev"]