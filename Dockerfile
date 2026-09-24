FROM python:3.12-slim

# Prevent Python from writing pyc files and buffering stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8000

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source code
COPY . .

# Working directory where manage.py is located
WORKDIR /app/website

# Collect static files during image build for WhiteNoise
RUN python manage.py collectstatic --noinput

# Expose port (default 8000 or Railway dynamic $PORT)
EXPOSE 8000

# Run migrations and start Gunicorn on the port provided by Railway ($PORT)
CMD ["sh", "-c", "python manage.py migrate && gunicorn website.wsgi:application --bind 0.0.0.0:${PORT:-8000} --workers 2 --threads 4 --timeout 60"]
