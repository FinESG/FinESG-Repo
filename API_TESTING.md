# Testing with Postman / HTTPie (Updated)

All endpoints now accept **JSON body** (no form-data).
Cookies are used for authentication after login.

---

## 1. Register (Create User)

**URL**: `POST http://127.0.0.1:8080/register`

**Headers**:
- `Content-Type: application/json`

**Body (JSON)**:
```json
{
    "email": "testuser@example.com",
    "password": "securepassword"
}
```

---

## 2. Login (Get Token + Cookie)

**URL**: `POST http://127.0.0.1:8080/login`

**Headers**:
- `Content-Type: application/json`

**Body (JSON)**:
```json
{
    "email": "testuser@example.com",
    "password": "securepassword"
}
```

**Response**: JWT Token + `access_token` cookie is set automatically.

> In Postman, the cookie is saved automatically. Future requests will include it.

---

## 3. Predict (Use Model)

**URL**: `POST http://127.0.0.1:8080/predict`

**Headers**:
- `Content-Type: application/json`
- Cookie is automatically sent by Postman after login.

**Body (JSON)**:
```json
{
    "text": "What is the future of AI?"
}
```

---

## 4. Get Chat History

**URL**: `GET http://127.0.0.1:8080/history`

No body needed. Cookie is sent automatically.

---

## HTTPie Commands

```bash
# 1. Register
http POST http://127.0.0.1:8080/register email=testuser@example.com password=securepassword

# 2. Login (saves cookie to session)
http --session=./session.json POST http://127.0.0.1:8080/login email=testuser@example.com password=securepassword

# 3. Predict (uses saved cookie)
http --session=./session.json POST http://127.0.0.1:8080/predict text="What is AI?"

# 4. History
http --session=./session.json GET http://127.0.0.1:8080/history
```
