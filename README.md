# PyReact Fusion Template

A production-ready full-stack application template combining Python FastAPI backend with React frontend, designed for rapid development and easy deployment.

## 🚀 Features

- **Modern Backend**: FastAPI with async support, automatic API documentation, and type hints
- **React Frontend**: React 18+ with Vite for fast development and optimized builds
- **Multi-Database Support**: SQLite (default), PostgreSQL, MySQL, and MongoDB
- **JWT Authentication**: Secure token-based authentication ready to use
- **Production Build**: Nuitka compilation for standalone executables
- **Tailwind CSS**: Modern, responsive UI with Tailwind CSS
- **Type Safety**: Pydantic models for request/response validation
- **CORS Configuration**: Pre-configured for development and production
- **Comprehensive Logging**: Structured logging with file and console output
- **Docker Support**: Containerized deployment ready

## 📋 Prerequisites

- **Python**: 3.9 or higher
- **Node.js**: 16.x or higher (for frontend development)
- **pnpm**: Package manager for frontend dependencies (recommended) or npm/yarn

### Optional (for specific databases):
- PostgreSQL 12+ (if using PostgreSQL)
- MySQL 8+ (if using MySQL)
- MongoDB 4.4+ (if using MongoDB)

## 🛠️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/skmercur/pyreact-fusion.git
cd pyreact-fusion
```

### 2. Backend Setup

```bash
# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Linux/Mac:
source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt
```

### 3. Frontend Setup

```bash
cd frontend
pnpm install
cd ..
```

### 4. Configuration

Copy the example environment file and configure it:

```bash
# Copy .env.example to .env
cp .env.example .env
```

Edit `.env` file with your configuration:

```env
ENVIRONMENT=development
DEBUG=true
DATABASE_TYPE=sqlite
JWT_SECRET_KEY=your-secret-key-change-in-production
```

## 🚀 Quick Start

### Initial Setup

First, run the interactive setup to configure your application:

```bash
python scripts/setup.py
```

This will guide you through:
- Choosing between Desktop mode (pywebview) or Web mode (browser)
- Setting up your application name, description, and version
- Configuring author information
- Selecting database type
- Configuring server settings

### Development Mode

Run the development server:

```bash
python scripts/dev.py
```

Or run the configured application:

```bash
python scripts/run.py
```

This will start the application in the mode you selected during setup (Desktop or Web).

This will start:
- Backend server at `http://localhost:8000`
- API documentation at `http://localhost:8000/api/docs`
- Frontend development server at `http://localhost:5173` (if running separately)

**Note**: For full development experience, run frontend separately:

```bash
# Terminal 1: Backend
python -m uvicorn backend.main:app --reload

# Terminal 2: Frontend
cd frontend
pnpm run dev
```

### Production Build

#### Build Frontend Only

```bash
python scripts/build_frontend.py
```

#### Build Complete Executable

```bash
python scripts/build_executable.py
```

This will:
1. Build the React frontend
2. Copy assets to backend
3. Compile Python backend to standalone executable using Nuitka

The executable will be in the `dist/` directory.

## 📁 Project Structure

```
pyreact-fusion/
├── backend/                 # Python FastAPI backend
│   ├── __init__.py
│   ├── main.py             # Application entry point
│   ├── api/                # API routes and middleware
│   │   ├── routes.py       # API endpoints
│   │   └── middleware.py   # CORS, auth middleware
│   ├── database/           # Database layer
│   │   ├── connection.py   # Database factory
│   │   ├── models.py       # ORM models
│   │   └── migrations/     # Database migrations
│   ├── services/           # Business logic
│   │   └── auth.py         # Authentication service
│   └── config.py           # Configuration management
├── frontend/               # React frontend
│   ├── public/            # Static assets
│   ├── src/               # Source code
│   │   ├── components/    # React components
│   │   ├── pages/         # Page components
│   │   ├── services/      # API client
│   │   └── utils/         # Utility functions
│   ├── package.json
│   └── vite.config.js
├── build_config/          # Build configuration
│   ├── nuitka_build.py    # Nuitka compilation script
│   └── requirements.txt
├── config/                # Configuration files
│   ├── database.yaml      # Database config templates
│   └── app.yaml           # Application config
├── scripts/                # Build and dev scripts
│   ├── dev.py             # Development server
│   ├── build_frontend.py  # Frontend build
│   └── build_executable.py # Complete build pipeline
├── .env.example           # Environment variables template
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## 🗄️ Database Configuration

### SQLite (Default)

No additional setup required. Database file will be created at `./data/app.db`.

### PostgreSQL

1. Install PostgreSQL and create a database:

```sql
CREATE DATABASE pyreact_fusion;
```

2. Update `.env`:

```env
DATABASE_TYPE=postgresql
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=pyreact_fusion
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_password
```

### MySQL

1. Install MySQL and create a database:

```sql
CREATE DATABASE pyreact_fusion CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

2. Update `.env`:

```env
DATABASE_TYPE=mysql
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_DB=pyreact_fusion
MYSQL_USER=root
MYSQL_PASSWORD=your_password
```

### MongoDB

1. Install MongoDB and start the service
2. Update `.env`:

```env
DATABASE_TYPE=mongodb
MONGODB_HOST=localhost
MONGODB_PORT=27017
MONGODB_DB=pyreact_fusion
MONGODB_USER=          # Optional
MONGODB_PASSWORD=      # Optional
```

## 🔐 Authentication

The template includes JWT-based authentication:

### Register a User

```bash
curl -X POST "http://localhost:8000/api/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "securepassword",
    "full_name": "Test User"
  }'
```

### Login

```bash
curl -X POST "http://localhost:8000/api/auth/login" \
  -H "Content-Type: multipart/form-data" \
  -F "username=testuser" \
  -F "password=securepassword"
```

### Access Protected Routes

```bash
curl -X GET "http://localhost:8000/api/users" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## 📡 API Endpoints

### Public Endpoints

- `GET /api/health` - Health check
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login and get access token

### Protected Endpoints (Require Authentication)

- `GET /api/auth/me` - Get current user information
- `GET /api/users` - Get list of users

### API Documentation

When running in development mode, visit:
- Swagger UI: `http://localhost:8000/api/docs`
- ReDoc: `http://localhost:8000/api/redoc`

## 🏗️ Building with Nuitka

### Prerequisites

```bash
pip install nuitka ordered-set
```

### Build Options

#### Onefile Mode (Single Executable)

```bash
python build_config/nuitka_build.py onefile
```

#### Standalone Mode (Directory with Dependencies)

```bash
python build_config/nuitka_build.py standalone
```

### Custom Build

Edit `build_config/nuitka_build.py` to customize:
- Included packages
- Data directories
- Plugins
- Output name and location

## 🐳 Docker Support

### Build Docker Image

```bash
docker build -t pyreact-fusion .
```

### Run Container

```bash
docker run -p 8000:8000 \
  -e DATABASE_TYPE=sqlite \
  -e JWT_SECRET_KEY=your-secret-key \
  pyreact-fusion
```

### Docker Compose

```bash
docker-compose up -d
```

## 🧪 Testing

### Backend Tests

```bash
# Install test dependencies
pip install pytest pytest-asyncio httpx

# Run tests
pytest backend/tests/
```

### Frontend Tests

```bash
cd frontend
pnpm test
```

## 📝 Environment Variables

Key environment variables (see `.env.example` for complete list):

| Variable | Description | Default |
|----------|-------------|---------|
| `ENVIRONMENT` | Environment mode (development/staging/production) | `development` |
| `DEBUG` | Enable debug mode | `true` |
| `DATABASE_TYPE` | Database type (sqlite/postgresql/mysql/mongodb) | `sqlite` |
| `JWT_SECRET_KEY` | Secret key for JWT tokens | (required) |
| `HOST` | Server host | `0.0.0.0` |
| `PORT` | Server port | `8000` |

## 🚢 Deployment

### Production Checklist

- [ ] Set `ENVIRONMENT=production` and `DEBUG=false`
- [ ] Change `JWT_SECRET_KEY` to a strong random secret
- [ ] Configure production database
- [ ] Set up proper CORS origins
- [ ] Configure logging
- [ ] Build frontend: `python scripts/build_frontend.py`
- [ ] Test the application
- [ ] Set up reverse proxy (nginx/Apache) if needed
- [ ] Configure SSL/TLS certificates

### Running in Production

```bash
# Using uvicorn directly
uvicorn backend.main:app --host 0.0.0.0 --port 8000 --workers 4

# Using the executable
./dist/pyreact-fusion
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👤 Author

**Sofiane Khoudour**

- GitHub: [@skmercur](https://github.com/skmercur/)
- Email: khoudoursofiane75@gmail.com

## 🙏 Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/) - Modern Python web framework
- [React](https://react.dev/) - JavaScript library for building user interfaces
- [Vite](https://vitejs.dev/) - Next generation frontend tooling
- [Nuitka](https://nuitka.net/) - Python compiler
- [Tailwind CSS](https://tailwindcss.com/) - Utility-first CSS framework

## 📚 Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://react.dev/)
- [Vite Documentation](https://vitejs.dev/)
- [Nuitka Documentation](https://nuitka.net/doc/)

## 🐛 Troubleshooting

### Frontend Build Fails

- Ensure Node.js 16+ is installed
- Delete `node_modules` and `pnpm-lock.yaml`, then run `pnpm install` again
- Check for version conflicts in `package.json`

### Database Connection Issues

- Verify database service is running
- Check connection credentials in `.env`
- Ensure database exists (for PostgreSQL/MySQL)
- Check firewall settings

### Nuitka Build Issues

- Ensure all dependencies are installed
- Check Python version (3.9+)
- Try building in standalone mode first
- Check Nuitka documentation for platform-specific issues

### Port Already in Use

- Change `PORT` in `.env` file
- Or stop the process using the port:
  - Windows: `netstat -ano | findstr :8000`
  - Linux/Mac: `lsof -i :8000`

---

**Happy Coding! 🎉**

