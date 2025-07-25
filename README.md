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

## 4. Refresh the Access Token (if needed)
- If your access token expires, use the refresh token to get a new one (endpoint not shown here, but can be added).

**Note:**
- Passwords are always hashed for security.
- Never share your tokens or password with anyone.
- If you get "Invalid credentials", check your username and password or register a new user. 