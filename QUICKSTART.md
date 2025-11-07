# Quick Start Guide

## 🚀 Get Started in 5 Minutes

### 1. Install Dependencies

**Backend:**
```bash
python -m venv venv
venv\Scripts\activate  # Windows
# or: source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
```

**Frontend:**
```bash
cd frontend
pnpm install
cd ..
```

### 2. Configure Environment

```bash
# Copy .env.example to .env
copy .env.example .env  # Windows
# or: cp .env.example .env  # Linux/Mac
```

Edit `.env` and set at minimum:
```env
JWT_SECRET_KEY=your-secret-key-here
```

### 3. Initial Setup (First Time Only)

Run the interactive setup:

```bash
python scripts/setup.py
```

This will ask you to:
- Choose Desktop or Web mode
- Enter app name, description, version
- Configure author information
- Select database type
- Set server configuration

### 4. Run Development Server

**Option A: Run Configured Application**
```bash
python scripts/run.py
```

**Option B: Backend Only**
```bash
python -m uvicorn backend.main:app --reload
```

**Option C: Both Frontend and Backend**
```bash
# Terminal 1: Backend
python -m uvicorn backend.main:app --reload

# Terminal 2: Frontend
cd frontend
pnpm run dev
```

### 5. Access the Application

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/api/docs

### 6. Test the Application

1. Visit http://localhost:8000/api/docs
2. Try the `/api/health` endpoint
3. Register a user via `/api/auth/register`
4. Login via `/api/auth/login`
5. Use the token to access protected endpoints

## 📦 Build for Production

### Build Frontend
```bash
python scripts/build_frontend.py
```

### Build Executable
```bash
python scripts/build_executable.py
```

The executable will be in the `dist/` directory.

## 🐳 Docker

```bash
docker-compose up -d
```

## 🧪 Run Tests

```bash
pytest backend/tests/
```

## 📚 Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Configure your database (see Database Configuration section)
- Customize the frontend components
- Add your own API endpoints
- Deploy to production

---

**Need Help?** Check the [README.md](README.md) or open an issue on GitHub.

