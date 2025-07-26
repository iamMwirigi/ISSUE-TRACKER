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

# Services Endpoints

All endpoints require the `Authorization: Bearer <access_token>` header.

## Create a Service
- **POST** `/api/services/create/`
- **Body:**
  ```json
  {
    "name": "Service Name",
    "description": "Service description"
  }
  ```
- **Response:**
  ```json
  {
    "id": "<service_id>",
    "name": "Service Name",
    "description": "Service description",
    "created_at": "2025-07-25T...",
    "message": "Service created successfully."
  }
  ```

## List Services
- **GET** `/api/services/list/`
- **Response:**
  ```json
  [
    {
      "id": "<service_id>",
      "name": "Service Name",
      "description": "Service description",
      "created_at": "2025-07-25T..."
    },
    ...
  ]
  ```

## Retrieve a Service
- **POST** `/api/services/retrieve/`
- **Body:**
  ```json
  { "id": "<service_id>" }
  ```
- **Response:**
  ```json
  {
    "id": "<service_id>",
    "name": "Service Name",
    "description": "Service description",
    "created_at": "2025-07-25T..."
  }
  ```

## Update a Service
- **POST** `/api/services/update/`
- **Body:**
  ```json
  {
    "id": "<service_id>",
    "name": "New Name",
    "description": "Updated description"
  }
  ```
- **Response:**
  ```json
  {
    "id": "<service_id>",
    "name": "New Name",
    "description": "Updated description",
    "created_at": "2025-07-25T...",
    "message": "Service updated successfully."
  }
  ```

## Delete a Service
- **POST** `/api/services/delete/`
- **Body:**
  ```json
  { "id": "<service_id>" }
  ```
- **Response:**
  ```json
  { "message": "Service deleted successfully." }
  ```

---

# Issues Endpoints

All endpoints require the `Authorization: Bearer <access_token>` header.

## Create an Issue
- **POST** `/api/issues/create/`
- **Body (FormData for file upload):**
  ```json
  {
    "type": "Printer Issue",
    "description": "The office printer is jammed.",
    "status": "unsolved", // or "solved"
    "service": "<service_id>",
    "office": "<office_id>", // optional
    "assigned_to": "<user_id>", // optional
    "attachments": "<file>" // optional - supports images, documents, etc.
  }
  ```
- **Response:**
  ```json
  {
    "id": "<issue_id>",
    "type": "Printer Issue",
    "description": "The office printer is jammed.",
    "status": "unsolved",
    "service": "<service_id>",
    "office": "<office_id>",
    "assigned_to": "<user_id>",
    "attachments": "/media/issue_attachments/filename.jpg",
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
      "type": "Printer Issue",
      "description": "The office printer is jammed.",
      "status": "unsolved",
      "reporter": "<user_id>",
      "service": "<service_id>",
      "office": "<office_id>",
      "assigned_to": "<user_id>",
      "attachments": "/media/issue_attachments/filename.jpg",
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
- For file uploads, use FormData instead of JSON and include the file in the `attachments` field.
- Supported file types: images (jpg, png, gif), documents (pdf, doc, docx), and other common formats.
- If you get an error, check the response for details and make sure your request matches the documented format. 