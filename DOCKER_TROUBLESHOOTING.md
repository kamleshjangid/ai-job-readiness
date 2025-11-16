# Docker Troubleshooting Guide

## ✅ **FIXED: Settings Configuration Error**

The error you encountered was due to missing configuration attributes in the settings. This has been fixed by updating the configuration structure.

## 🚀 **Updated Commands to Run the Project**

### **1. Clean Start (Recommended)**
```bash
# Stop and remove all containers
docker-compose down -v

# Rebuild and start fresh
docker-compose up --build -d

# Check logs
docker-compose logs -f
```

### **2. Quick Restart (If Already Running)**
```bash
# Restart just the backend
docker-compose restart backend

# Or restart all services
docker-compose restart
```

### **3. Check Service Status**
```bash
# See all running containers
docker-compose ps

# Check specific service logs
docker-compose logs backend
docker-compose logs frontend
docker-compose logs database
```

## 🔧 **What Was Fixed**

The error occurred because the settings configuration was restructured but some files were still trying to access the old flat structure. Fixed:

1. **`app/core/users.py`** - Updated to use `settings.security.*` instead of `settings.*`
2. **`app/core/security.py`** - Updated all security-related settings to use nested structure

## 📊 **Expected Output After Fix**

When you run `docker-compose up -d`, you should see:

```bash
# Database starts
database-1   | PostgreSQL init process complete; ready for start up.

# Backend starts successfully
backend-1    | Waiting for database to be ready...
backend-1    | Running Alembic migrations...
backend-1    | INFO:     Uvicorn running on http://0.0.0.0:8000

# Frontend starts
frontend-1   | Compiled successfully!
frontend-1   | You can now view frontend in the browser.
```

## 🌐 **Access Your Application**

After successful startup:
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Database**: localhost:5432

## 🧪 **Test the Fix**

```bash
# Test backend health
curl http://localhost:8000/health

# Test API info
curl http://localhost:8000/api/v1/info

# Test frontend
open http://localhost:3000
```

## 🚨 **If You Still Get Errors**

### **1. Complete Reset**
```bash
# Stop everything
docker-compose down -v

# Remove all images
docker system prune -a

# Start fresh
docker-compose up --build -d
```

### **2. Check Docker Resources**
```bash
# Check Docker is running
docker --version

# Check available space
docker system df

# Check running containers
docker ps
```

### **3. Manual Database Check**
```bash
# Connect to database directly
docker-compose exec database psql -U postgres -d ai_job_readiness

# Check if tables exist
\dt

# Exit database
\q
```

## 📝 **Environment Variables (Optional)**

Create a `.env` file in the project root for custom configuration:

```bash
# .env file
POSTGRES_PASSWORD=your_secure_password
SECRET_KEY=your_secret_key_here
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## 🎯 **Quick Success Checklist**

- [ ] Docker is running
- [ ] No port conflicts (8000, 3000, 5432)
- [ ] Sufficient disk space
- [ ] All containers start without errors
- [ ] Backend responds to health check
- [ ] Frontend loads in browser

---

**The configuration issue has been resolved! 🎉**

Run `docker-compose up --build -d` and your application should start successfully.
