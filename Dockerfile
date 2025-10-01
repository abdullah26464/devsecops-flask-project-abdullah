# Use pinned official Python image (slim for smaller size)
FROM python:3.9-slim-bullseye

# Install required packages in one RUN to reduce layers and cleanup apt cache
RUN apt-get update && apt-get install -y \
    nginx \
    python3-dev \
    build-essential \
    uwsgi \
    uwsgi-plugin-python3 \
    && rm -rf /var/lib/apt/lists/*

# Copy nginx config
COPY conf/nginx.conf /etc/nginx/nginx.conf

# Copy app and set ownership to www-data for security (not root)
COPY --chown=www-data:www-data . /srv/flask_app

WORKDIR /srv/flask_app

# Install Python dependencies (consider using a virtual environment for production)
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port
EXPOSE 5000

# Use non-root user www-data
USER www-data

# Add health check for container orchestration
HEALTHCHECK --interval=30s --timeout=5s \
    CMD curl -f http://localhost:5000/health || exit 1

# Start nginx and uwsgi server
CMD service nginx start && uwsgi --ini uwsgi.ini
