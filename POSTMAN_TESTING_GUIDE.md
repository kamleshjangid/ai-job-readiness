# AI Job Readiness API - Postman Testing Guide

## 🚀 Quick Start

### 1. Import Collection
1. Open Postman
2. Click "Import" button
3. Select the `AI_Job_Readiness_API.postman_collection.json` file
4. The collection will be imported with all endpoints organized by category

### 2. Set Environment Variables
Before testing, set these variables in Postman:

| Variable | Value | Description |
|----------|-------|-------------|
| `base_url` | `http://localhost:8000` | API base URL |
| `access_token` | (auto-filled) | JWT access token |
| `refresh_token` | (auto-filled) | JWT refresh token |
| `user_id` | (auto-filled) | User ID for testing |
| `role_id` | (auto-filled) | Role ID for testing |
| `resume_id` | (auto-filled) | Resume ID for testing |
| `score_id` | (auto-filled) | Score ID for testing |

## 📋 Testing Workflow

### Step 1: Health Check
1. **Root Endpoint** - `GET /` - Basic API status
2. **Health Check** - `GET /health` - Detailed health information
3. **Database Status** - `GET /database` - Database connectivity
4. **API Info** - `GET /api/v1/info` - API information

### Step 2: Authentication
1. **Register User** - `POST /api/v1/auth/register`
   ```json
   {
     "email": "test@example.com",
     "password": "testpassword123",
     "first_name": "John",
     "last_name": "Doe",
     "phone": "+1234567890",
     "bio": "Software Developer with 5 years experience"
   }
   ```

2. **Login User** - `POST /api/v1/auth/jwt/login`
   - Use form-data with username and password
   - Copy the `access_token` and `refresh_token` from response

3. **Get Current User** - `GET /api/v1/users/me`
   - Add `Authorization: Bearer {{access_token}}` header

### Step 3: User Management
1. **Get User Profile** - `GET /api/v1/users/profile`
2. **Update User Profile** - `PUT /api/v1/users/profile`
3. **List Users** - `GET /api/v1/users/list` (Admin only)

### Step 4: Role Management
1. **Create Role** - `POST /api/v1/roles/`
   ```json
   {
     "name": "test_role",
     "description": "Test role for API testing",
     "permissions": ["read", "write", "update"]
   }
   ```

2. **Get All Roles** - `GET /api/v1/roles/`
3. **Update Role** - `PUT /api/v1/roles/{{role_id}}`
4. **Assign Role to User** - `POST /api/v1/roles/assign`

### Step 5: Resume Management
1. **Create Resume** - `POST /api/v1/resumes/`
   ```json
   {
     "title": "Software Developer Resume",
     "summary": "Experienced software developer with 5 years of experience",
     "experience_years": 5.0,
     "education_level": "Bachelor's Degree",
     "skills": ["Python", "JavaScript", "React", "Node.js", "SQL"],
     "languages": ["English", "Spanish"],
     "is_public": true
   }
   ```

2. **List User Resumes** - `GET /api/v1/resumes/`
3. **Get Resume by ID** - `GET /api/v1/resumes/{{resume_id}}`
4. **Update Resume** - `PUT /api/v1/resumes/{{resume_id}}`
5. **Upload Resume File** - `POST /api/v1/resumes/{{resume_id}}/upload`
6. **Analyze Resume** - `POST /api/v1/resumes/{{resume_id}}/analyze`

### Step 6: Score Management
1. **Create Score** - `POST /api/v1/scores/`
   ```json
   {
     "resume_id": 1,
     "analysis_type": "comprehensive",
     "job_title": "Senior Software Developer",
     "company": "Tech Corp",
     "overall_score": 85.5,
     "skill_score": 90.0,
     "experience_score": 80.0,
     "education_score": 85.0,
     "skill_matches": ["Python", "JavaScript", "React"],
     "skill_gaps": ["Docker", "Kubernetes"],
     "recommendations": "Consider learning containerization technologies"
   }
   ```

2. **Get User Scores** - `GET /api/v1/scores/`
3. **Get Score by ID** - `GET /api/v1/scores/{{score_id}}`
4. **Update Score** - `PUT /api/v1/scores/{{score_id}}`

## 🔧 Environment Setup

### Backend Setup
```bash
# Start the backend server
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Database Setup
```bash
# Run database migrations
cd backend
alembic upgrade head
```

## 📊 Expected Responses

### Success Response Format
```json
{
  "success": true,
  "message": "Operation completed successfully",
  "data": {
    // Response data here
  },
  "timestamp": "2024-12-01T10:00:00Z"
}
```

### Error Response Format
```json
{
  "success": false,
  "message": "Error description",
  "error": "Detailed error information",
  "timestamp": "2024-12-01T10:00:00Z"
}
```

## 🧪 Test Scenarios

### 1. Complete User Journey
1. Register a new user
2. Login and get tokens
3. Update user profile
4. Create a resume
5. Upload resume file
6. Analyze resume
7. Create score for resume
8. View all user data

### 2. Admin Operations
1. Login as admin user
2. List all users
3. Create new role
4. Assign role to user
5. View role statistics

### 3. Error Handling
1. Try to access protected route without token
2. Try to create duplicate user
3. Try to access non-existent resource
4. Try to update with invalid data

## 🔍 Performance Testing

### 1. Cache Testing
1. **Cache Status** - `GET /api/v1/cache/status`
2. **Clear Cache** - `POST /api/v1/cache/clear`
3. **Performance Metrics** - `GET /api/v1/performance`

### 2. Load Testing
- Use Postman Runner to run multiple requests
- Test pagination with large datasets
- Test concurrent user operations

## 📝 Notes

### Authentication
- All protected endpoints require `Authorization: Bearer {{access_token}}` header
- Tokens expire after 30 minutes (configurable)
- Use refresh token to get new access token

### Pagination
- Most list endpoints support pagination
- Use `page` and `per_page` (or `size`) parameters
- Default page size is 10, maximum is 100

### File Upload
- Resume file upload supports common formats (PDF, DOC, DOCX)
- Maximum file size is 10MB (configurable)
- Files are stored in `backend/uploads/resumes/` directory

### Data Validation
- All input data is validated using Pydantic schemas
- Invalid data returns 422 Unprocessable Entity
- Required fields are clearly documented

## 🚨 Troubleshooting

### Common Issues

1. **401 Unauthorized**
   - Check if access token is valid
   - Try refreshing the token
   - Ensure Authorization header is correct

2. **422 Validation Error**
   - Check request body format
   - Ensure all required fields are provided
   - Validate data types and formats

3. **500 Internal Server Error**
   - Check backend logs
   - Ensure database is running
   - Verify all dependencies are installed

4. **Connection Refused**
   - Ensure backend server is running on port 8000
   - Check if database is accessible
   - Verify environment variables

### Debug Tips
- Use Postman Console to see detailed request/response logs
- Check backend terminal for error messages
- Use the `/health` endpoint to verify system status
- Check database connectivity with `/database` endpoint

## 📚 Additional Resources

- **API Documentation**: http://localhost:8000/docs (Swagger UI)
- **ReDoc Documentation**: http://localhost:8000/redoc
- **OpenAPI Schema**: http://localhost:8000/openapi.json

---

**Happy Testing! 🎉**

For any issues or questions, check the backend logs or refer to the comprehensive README.md file.
