# Set the python version as a build-time argument
# with Python 3.12 as the default
ARG PYTHON_VERSION=3.12-slim
FROM python:${PYTHON_VERSION}

# Create a virtual environment
RUN python -m venv /opt/venv

# Set the virtual environment as the current location
ENV PATH=/opt/venv/bin:$PATH

# Upgrade pip
RUN pip install --upgrade pip

# Set Python-related environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install os dependencies for our mini vm
RUN apt-get update && apt-get install -y \
    # for postgres
    libpq-dev \
    # for Pillow
    libjpeg-dev \
    # for CairoSVG
    libcairo2 \
    # for health checks
    curl \
    # other
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Create the mini vm's code directory
RUN mkdir -p /code

# Set the working directory to that same code directory
WORKDIR /code

# Create a non-root user for security
RUN useradd --create-home --shell /bin/bash django && chown -R django:django /code /opt/venv
USER django

# create a bash script to run the Django project
# this script will execute at runtime when
# the container starts and the database is available
RUN printf "#!/bin/bash\n" > ./paracord_runner.sh && \
    printf "set -e\n\n" >> ./paracord_runner.sh && \
    printf "RUN_PORT=\"\${PORT:-8000}\"\n\n" >> ./paracord_runner.sh && \
    printf "echo \"Running database migrations...\"\n" >> ./paracord_runner.sh && \
    printf "python manage.py migrate --no-input\n\n" >> ./paracord_runner.sh && \
    printf "echo \"Collecting static files...\"\n" >> ./paracord_runner.sh && \
    printf "python manage.py collectstatic --no-input --clear\n\n" >> ./paracord_runner.sh && \
    printf "echo \"Starting Gunicorn server on port \$RUN_PORT...\"\n" >> ./paracord_runner.sh && \
    printf "exec gunicorn saas.wsgi:application --bind \"0.0.0.0:\$RUN_PORT\" --workers 2 --threads 4 --max-requests 1000 --max-requests-jitter 50 --log-level info\n" >> ./paracord_runner.sh

# make the bash script executable
RUN chmod +x paracord_runner.sh

# Clean up apt cache to reduce image size
RUN apt-get remove --purge -y \
    && apt-get autoremove -y \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file into the container
COPY requirements.txt /tmp/requirements.txt

# copy the project code into the container's working directory
COPY ./src /code

# Install the Python project requirements
RUN pip install -r /tmp/requirements.txt

# Create a non-root user for security
RUN useradd --create-home --shell /bin/bash django && chown -R django:django /code /opt/venv
USER django

# Add health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:${PORT:-8000}/ || exit 1

# Run the Django project via the runtime script
# when the container starts
CMD ./paracord_runner.sh