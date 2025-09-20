.PHONY: help setup dev prod clean test migrate superuser shell collectstatic

# Default target
help:
	@echo "Available commands:"
	@echo "  setup      - Set up development environment"
	@echo "  dev        - Start development server with Docker"
	@echo "  prod       - Build production Docker image"
	@echo "  clean      - Clean up temporary files"
	@echo "  test       - Run tests"
	@echo "  migrate    - Run database migrations"
	@echo "  superuser  - Create Django superuser"
	@echo "  shell      - Open Django shell"
	@echo "  collectstatic - Collect static files"

# Set up development environment
setup:
	@echo "Setting up development environment..."
	@cd src && python -m venv venv
	@cd src && source venv/bin/activate && pip install -r ../requirements.txt
	@echo "✅ Development environment setup complete!"
	@echo "Run 'make dev' to start the development server"

# Start development server
dev:
	@echo "Starting development server..."
	docker-compose up --build

# Build production image
prod:
	@echo "Building production image..."
	docker build -t saas-app .

# Clean up temporary files
clean:
	@echo "Cleaning up..."
	@find . -type f -name "*.pyc" -delete
	@find . -type d -name "__pycache__" -delete
	@find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	@echo "✅ Cleanup complete!"

# Run tests
test:
	@echo "Running tests..."
	@cd src && python manage.py test

# Run migrations
migrate:
	@echo "Running migrations..."
	@cd src && python manage.py migrate

# Create superuser
superuser:
	@echo "Creating superuser..."
	@cd src && python manage.py createsuperuser

# Open Django shell
shell:
	@echo "Opening Django shell..."
	@cd src && python manage.py shell

# Collect static files
collectstatic:
	@echo "Collecting static files..."
	@cd src && python manage.py collectstatic --no-input