# MLFlow Dockerfile
FROM python:3.12-slim-bookworm

# Create a user
RUN useradd -m appuser
WORKDIR /home/appuser

# Install required system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl ca-certificates libpq-dev gcc python3-dev && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Switch to non-root user
USER appuser

# Set up virtual environment
RUN python -m venv venv
ENV PATH="/home/appuser/venv/bin:$PATH"

# Install Python dependencies
RUN pip install --no-cache-dir \
    mlflow[extras]==2.20.2 \
    psycopg2==2.9.10 \
    boto3==1.36.21 \
    cryptography==44.0.1 \
    pymysql==1.1.1 \
    scikit-learn==1.6.1 \
    loguru==0.7.3 \
    xgboost==2.1.4