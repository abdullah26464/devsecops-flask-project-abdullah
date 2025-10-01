# Use pinned Python image
FROM python:3.9-slim-bullseye

# Install required system packages in one layer
RUN apt-get update && apt-get install -y --no-install-recommends \
    nginx \
    python3-dev \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy nginx config
COPY conf/nginx.conf /etc/nginx/nginx.conf

# Copy app into /srv/flask_app and set ownership
WORKDIR /srv/flask_app
COPY . /srv/flask_app
RUN chown -R www-data:www-data /srv/flask_app

# Install Python dependencies
# ✅ Install uwsgi from pip instead of apt (safer & more up-to-date)
RUN pip install --no-cache-dir -r requirements.txt \
    && pip install --no-cache-dir uwsgi

# Expose uwsgi/nginx port (use 80 since nginx will listen there)
EXPOSE 80

# Switch to non-root user
USER www-data

# Healthcheck (using curl, now installed)
HEALTHCHECK --interval=30s --timeout=5s \
    CMD curl -f http://localhost/health || exit 1

# Start nginx and uwsgi in the foreground
CMD nginx -g 'daemon off;' & uwsgi --ini uwsgi.ini
