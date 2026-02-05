# Stage 1: Builder - Install dependencies
FROM python:3.11-slim AS builder

WORKDIR /app

# Copy requirements first for caching
COPY requirements.txt .

# Create virtualenv and install deps
RUN python -m venv /opt/venv \
    && . /opt/venv/bin/activate \
    && pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Stage 2: Runtime - Slim production image
FROM python:3.11-slim

WORKDIR /app

# Copy venv from builder
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy app code
COPY . .

# Expose port
EXPOSE 8000

# Healthcheck for AWS ECS/load balancers
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

