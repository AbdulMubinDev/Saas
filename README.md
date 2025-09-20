# SaaS Django Application

A Django-based SaaS application with PostgreSQL database, designed for both development and production deployment.

## 🚀 Quick Start

### Option 1: Docker Compose (Recommended for Development)

1. **Clone and navigate to the project:**
   ```bash
   cd Saas
   ```

2. **Start the development environment:**
   ```bash
   docker-compose up --build
   ```

3. **Access the application:**
   - Web App: http://localhost:8000
   - Admin: http://localhost:8000/admin

### Option 2: Local Development (Python Virtual Environment)

1. **Create and activate virtual environment:**
   ```bash
   cd Saas/src
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies:**
   ```bash
   pip install -r ../requirements.txt
   ```

3. **Set up environment variables:**
   ```bash
   cp ../.env.development .env
   ```

4. **Run migrations and start server:**
   ```bash
   python manage.py migrate
   python manage.py collectstatic --no-input
   python manage.py runserver
   ```

## 🏭 Production Deployment (Railway)

### Automatic Deployment

1. **Push to Railway:**
   ```bash
   railway login
   railway init
   railway up
   ```

2. **Set Environment Variables in Railway Dashboard:**
   - `DJANGO_DEBUG=False`
   - `DJANGO_SECRET_KEY` (Generate a secure key)
   - `DATABASE_URL` (PostgreSQL connection string)
   - `CONN_MAX_AGE=30`

### Manual Deployment

1. **Build and push Docker image:**
   ```bash
   docker build -t your-app-name .
   docker tag your-app-name registry.railway.app/your-project-id/your-app-name
   docker push registry.railway.app/your-project-id/your-app-name
   ```

2. **Deploy on Railway:**
   - Use the Railway dashboard to deploy the Docker image
   - Configure environment variables as mentioned above

## 📁 Project Structure

```
Saas/
├── src/                    # Django project source code
│   ├── saas/              # Main Django project
│   ├── home/              # Home app
│   ├── command/           # Command app
│   ├── staticfiles/       # Static files directory
│   └── manage.py
├── Dockerfile             # Production Docker configuration
├── docker-compose.yml     # Development Docker configuration
├── requirements.txt       # Python dependencies
├── .env                   # Production environment variables
├── .env.development       # Development environment variables
└── README.md
```

## 🔧 Configuration

### Environment Variables

| Variable | Development | Production | Description |
|----------|-------------|------------|-------------|
| `DJANGO_DEBUG` | `True` | `False` | Enable/disable debug mode |
| `DJANGO_SECRET_KEY` | Dev key | Secure key | Django secret key |
| `DATABASE_URL` | `sqlite:///db.sqlite3` | PostgreSQL URL | Database connection |
| `CONN_MAX_AGE` | `0` | `30` | Database connection age |

### Static Files

- **Development**: Files served from `staticfiles/` directory
- **Production**: Files collected to `staticfiles_collected/` and served by Whitenoise

## 🛠 Development Commands

```bash
# Run tests
python manage.py test

# Create migrations
python manage.py makemigrations

# Run migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic

# Create superuser
python manage.py createsuperuser

# Run Django shell
python manage.py shell
```

## 🔒 Security Notes

1. **Never commit secret keys** to version control
2. **Use HTTPS in production** for secure connections
3. **Keep dependencies updated** for security patches
4. **Use environment variables** for sensitive configuration

## 📊 Monitoring

- **Health Check**: Available at `/` (configured in Dockerfile)
- **Admin Panel**: Available at `/admin` (requires authentication)
- **Static Files**: Served efficiently with Whitenoise in production

## 🐛 Troubleshooting

### Common Issues

1. **Static files not loading**: Run `python manage.py collectstatic`
2. **Database connection issues**: Check `DATABASE_URL` environment variable
3. **Permission errors**: Ensure proper file permissions in Docker containers

### Logs

- **Development**: Check Django development server output
- **Production**: Check Railway deployment logs
- **Docker**: Use `docker-compose logs` for container logs

## 📝 License

This project is licensed under the MIT License.