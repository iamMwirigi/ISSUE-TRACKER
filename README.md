# Authentication Guide (For Junior Developers)

## 1. Register a New User
- **Endpoint:** `POST /api/auth/register/`
- **Body (JSON):**
  ```json
  {
    "username": "your_username",
    "phone_number": "0712345678",
    "password": "your_password"
  }
  ```
- **Response:**
  ```json
  { "detail": "User created successfully." }
  ```

## 2. Login
- **Endpoint:** `POST /api/auth/login/`
- **Body (JSON):**
  ```json
  {
    "username": "your_username",
    "password": "your_password"
  }
  ```
- **Response:**
  ```json
  {
    "refresh": "<refresh_token>",
    "access": "<access_token>",
    "role": "admin" // or "user"
  }
  ```

## 3. Use the Access Token
- For any protected API, add this header:
  ```
  Authorization: Bearer <access_token>
  ```

---

# Projects Endpoints

All endpoints require the `Authorization: Bearer <access_token>` header.

## Create a Project
- **POST** `/api/projects/create/`
- **Body:**
  ```json
  {
    "name": "Project Name",
    "description": "Project description"
  }
  ```
- **Response:**
  ```json
  {
    "id": "<project_id>",
    "name": "Project Name",
    "description": "Project description",
    "created_at": "2025-07-25T...",
    "message": "Project created successfully."
  }
  ```

## List Projects
- **GET** `/api/projects/list/`
- **Response:**
  ```json
  [
    {
      "id": "<project_id>",
      "name": "Project Name",
      "description": "Project description",
      "created_at": "2025-07-25T..."
    },
    ...
  ]
  ```

## Retrieve a Project
- **POST** `/api/projects/retrieve/`
- **Body:**
  ```json
  { "id": "<project_id>" }
  ```
- **Response:**
  ```json
  {
    "id": "<project_id>",
    "name": "Project Name",
    "description": "Project description",
    "created_at": "2025-07-25T..."
  }
  ```

## Update a Project
- **POST** `/api/projects/update/`
- **Body:**
  ```json
  {
    "id": "<project_id>",
    "name": "New Name",
    "description": "Updated description"
  }
  ```
- **Response:**
  ```json
  {
    "id": "<project_id>",
    "name": "New Name",
    "description": "Updated description",
    "created_at": "2025-07-25T...",
    "message": "Project updated successfully."
  }
  ```

## Delete a Project
- **POST** `/api/projects/delete/`
- **Body:**
  ```json
  { "id": "<project_id>" }
  ```
- **Response:**
  ```json
  { "message": "Project deleted successfully." }
  ```

---

# Issues Endpoints

All endpoints require the `Authorization: Bearer <access_token>` header.

## Create an Issue
- **POST** `/api/issues/create/`
- **Body:**
  ```json
  {
    "title": "Printer not working",
    "description": "The office printer is jammed.",
    "status": "unsolved", // or "solved"
    "project": "<project_id>",
    "assigned_to": "<user_id>" // optional
  }
  ```
- **Response:**
  ```json
  {
    "id": "<issue_id>",
    "title": "Printer not working",
    "description": "The office printer is jammed.",
    "status": "unsolved",
    "project": "<project_id>",
    "assigned_to": "<user_id>",
    "created_at": "2025-07-25T...",
    "message": "Issue created successfully."
  }
  ```

## List Issues
- **GET** `/api/issues/list/`
- **Response:**
  ```json
  [
    {
      "id": "<issue_id>",
      "title": "Printer not working",
      "description": "The office printer is jammed.",
      "status": "unsolved",
      "reporter": "<user_id>",
      "project": "<project_id>",
      "assigned_to": "<user_id>",
      "created_at": "2025-07-25T..."
    },
    ...
  ]
  ```

---

**Tips:**
- Always use the correct field values (e.g., `status` must be "solved" or "unsolved").
- All endpoints require a valid JWT access token in the `Authorization` header.
- Use the returned `id` from create/list endpoints for retrieve, update, and delete.
- If you get an error, check the response for details and make sure your request matches the documented format. 