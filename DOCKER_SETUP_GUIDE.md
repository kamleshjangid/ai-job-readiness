# AI Job Readiness Platform - Docker Setup Guide

## 🐳 Quick Start Commands

### 1. **Start All Services (Recommended)**
```bash
# Start all services (database, backend, frontend)
docker-compose up -d

# View logs
docker-compose logs -f

# Stop all services
docker-compose down
```

### 2. **Start Specific Services**
```bash
# Start only database and backend
docker-compose up -d database backend

# Start only frontend (after backend is running)
docker-compose up -d frontend

# Start with rebuild
docker-compose up --build -d
```

### 3. **Development Commands**
```bash
# Rebuild and restart all services
docker-compose up --build --force-recreate -d

# View logs for specific service
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f database

# Execute commands in running containers
docker-compose exec backend bash
docker-compose exec frontend sh
docker-compose exec database psql -U postgres -d ai_job_readiness
```

## 🚀 Complete Setup Process

### Step 1: Prerequisites
```bash
# Ensure Docker and Docker Compose are installed
docker --version
docker-compose --version

# If not installed, install Docker Desktop or Docker Engine
# Visit: https://docs.docker.com/get-docker/
```

### Step 2: Clone and Navigate
```bash
# Navigate to project directory
cd ai-job-readiness

# Verify Docker files exist
ls -la docker-compose.yml
ls -la backend/Dockerfile
ls -la frontend/Dockerfile
```

### Step 3: Environment Setup
```bash
# Create environment file (optional - defaults are provided)
cat > .env << EOF
# Database Configuration
POSTGRES_DB=ai_job_readiness
POSTGRES_USER=postgres
POSTGRES_PASSWORD=password

# Backend Configuration
DATABASE_URL=postgresql+asyncpg://postgres:password@database:5432/ai_job_readiness
SECRET_KEY=your-secret-key-here
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30

# Frontend Configuration
REACT_APP_API_URL=http://localhost:8000
EOF
```

### Step 4: Start the Application
```bash
# Build and start all services
docker-compose up --build -d

# Check if all services are running
docker-compose ps
```

### Step 5: Verify Services
```bash
# Check backend health
curl http://localhost:8000/health

# Check frontend (in browser)
open http://localhost:3000

# Check database connection
docker-compose exec database pg_isready -U postgres
```

## 🔧 Service Details

### **Database Service (PostgreSQL)**
- **Port**: 5432
- **Database**: ai_job_readiness
- **User**: postgres
- **Password**: password
- **Health Check**: Automatic with pg_isready

### **Backend Service (FastAPI)**
- **Port**: 8000
- **URL**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Features**: Auto-migration, hot reload, health checks

### **Frontend Service (React)**
- **Port**: 3000
- **URL**: http://localhost:3000
- **Features**: Hot reload, development server

## 📊 Monitoring Commands

### **View All Logs**
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f database
```

### **Check Service Status**
```bash
# List running containers
docker-compose ps

# Check resource usage
docker stats

# Inspect specific container
docker-compose exec backend ps aux
```

### **Database Operations**
```bash
# Connect to database
docker-compose exec database psql -U postgres -d ai_job_readiness

# Run migrations manually
docker-compose exec backend alembic upgrade head

# Create new migration
docker-compose exec backend alembic revision --autogenerate -m "description"
```

## 🛠️ Development Workflow

### **Hot Reload Development**
```bash
# Start with volume mounts for development
docker-compose up -d

# Backend changes are auto-reloaded
# Frontend changes are auto-reloaded
# Database changes require container restart
```

### **Rebuild After Changes**
```bash
# Rebuild specific service
docker-compose build backend
docker-compose up -d backend

# Rebuild all services
docker-compose build
docker-compose up -d
```

### **Reset Everything**
```bash
# Stop and remove all containers, networks, volumes
docker-compose down -v

# Remove all images (optional)
docker-compose down --rmi all

# Start fresh
docker-compose up --build -d
```

## 🧪 Testing with Docker

### **Run Tests**
```bash
# Backend tests
docker-compose exec backend pytest tests/ -v

# Frontend tests
docker-compose exec frontend npm test

# Integration tests
docker-compose exec backend pytest tests/integration/ -v
```

### **API Testing**
```bash
# Test API endpoints
curl http://localhost:8000/health
curl http://localhost:8000/api/v1/info

# Test with Postman collection
# Import: AI_Job_Readiness_API.postman_collection.json
# Base URL: http://localhost:8000
```

## 🔍 Troubleshooting

### **Common Issues**

#### **Port Already in Use**
```bash
# Check what's using the port
lsof -i :8000
lsof -i :3000
lsof -i :5432

# Kill process or change ports in docker-compose.yml
```

#### **Database Connection Issues**
```bash
# Check database logs
docker-compose logs database

# Restart database
docker-compose restart database

# Check database health
docker-compose exec database pg_isready -U postgres
```

#### **Backend Not Starting**
```bash
# Check backend logs
docker-compose logs backend

# Check if migrations ran
docker-compose exec backend alembic current

# Run migrations manually
docker-compose exec backend alembic upgrade head
```

#### **Frontend Not Loading**
```bash
# Check frontend logs
docker-compose logs frontend

# Check if backend is accessible
curl http://localhost:8000/health

# Restart frontend
docker-compose restart frontend
```

### **Clean Up Commands**
```bash
# Remove all containers and networks
docker-compose down

# Remove everything including volumes
docker-compose down -v

# Remove all images
docker system prune -a

# Remove specific images
docker rmi ai-job-readiness_backend
docker rmi ai-job-readiness_frontend
```

## 📝 Environment Variables

### **Backend Environment**
```bash
DATABASE_URL=postgresql+asyncpg://postgres:password@database:5432/ai_job_readiness
SECRET_KEY=your-secret-key-here
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30
JWT_REFRESH_TOKEN_EXPIRE_DAYS=7
CORS_ORIGINS=["http://localhost:3000"]
```

### **Frontend Environment**
```bash
REACT_APP_API_URL=http://localhost:8000
REACT_APP_APP_NAME=AI Job Readiness
REACT_APP_VERSION=1.0.0
```

## 🚀 Production Deployment

### **Production Docker Compose**
```yaml
# docker-compose.prod.yml
version: '3.8'
services:
  database:
    image: postgres:15
    environment:
      POSTGRES_DB: ai_job_readiness
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
    volumes:
      - pgdata:/var/lib/postgresql/data
    networks:
      - app-network

  backend:
    build: ./backend
    environment:
      - DATABASE_URL=postgresql+asyncpg://postgres:${POSTGRES_PASSWORD}@database:5432/ai_job_readiness
      - SECRET_KEY=${SECRET_KEY}
    depends_on:
      - database
    networks:
      - app-network

  frontend:
    build: ./frontend
    environment:
      - REACT_APP_API_URL=${API_URL}
    networks:
      - app-network
```

### **Deploy to Production**
```bash
# Use production compose file
docker-compose -f docker-compose.prod.yml up -d

# Scale services
docker-compose -f docker-compose.prod.yml up -d --scale backend=3
```

## 📋 Quick Reference

### **Essential Commands**
```bash
# Start everything
docker-compose up -d

# View logs
docker-compose logs -f

# Stop everything
docker-compose down

# Rebuild and restart
docker-compose up --build -d

# Check status
docker-compose ps

# Access services
curl http://localhost:8000/health
open http://localhost:3000
```

### **Service URLs**
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Database**: localhost:5432

---

**Ready to go! 🚀**

Run `docker-compose up -d` and your AI Job Readiness Platform will be running on:
- Frontend: http://localhost:3000
- Backend: http://localhost:8000
- Database: localhost:5432
