FROM python:3.11-slim

WORKDIR /app

# Install system dependencies for scientific libraries & ReportLab
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Ensure data directory exists for SQLite development persistence
RUN mkdir -p /app/data

EXPOSE 8000

ENV PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app \
    DATABASE_URL=sqlite:///./data/ecosphere.db \
    ENABLE_BACKGROUND_SCHEDULER=true

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
