# 📚 Books API

A production-structured REST API built with **FastAPI**, featuring JWT authentication, argon2 password hashing, and SQLite database persistence with interactive auto-generated docs.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Framework | FastAPI |
| Database | SQLite via SQLAlchemy |
| Authentication | JWT (PyJWT) |
| Password Hashing | pwdlib + argon2 |
| Validation | Pydantic v2 |
| Server | Uvicorn |

---

## Features

- JWT-based authentication with bearer tokens
- Argon2 password hashing (winner of the Password Hashing Competition)
- Timing-attack-safe login with dummy hash verification
- Protected routes via FastAPI dependency injection
- Auto-generated Swagger UI at `/docs`
- Full CRUD for books
- Input validation with Pydantic Field constraints
- User registration with duplicate detection
- Active/disabled user flag support

---

## Project Structure

```
├── main.py            # Routes and app entry point
├── auth.py            # JWT creation, password hashing, auth dependencies
├── database.py        # SQLAlchemy engine, session, and DbDep alias
├── models.py          # SQLAlchemy table definitions (User, Book)
├── schemas.py         # Pydantic request/response models
└── requirements.txt   # Dependencies
```

---

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/ShubhPatel06/FAST-API-Practice-Tutorial.git
cd FAST-API-Practice-Tutorial
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv --without-pip

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the server

```bash
uvicorn main:app --reload
```

Visit **http://127.0.0.1:8000/docs** for the interactive Swagger UI.

---

## API Endpoints

### Auth

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| POST | `/register` | No | Create a new user |
| POST | `/token` | No | Login and receive JWT token |
| GET | `/users/me` | Yes | Get current user profile |

### Books

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/books` | No | Get all books |
| GET | `/books/{id}` | No | Get a single book |
| GET | `/books/search/` | No | Search by rating and/or author |
| POST | `/books` | Yes | Create a new book |
| PUT | `/books/{id}` | Yes | Update a book |
| DELETE | `/books/{id}` | Yes | Delete a book |

---

## Authentication Flow

```
1. POST /register        → create account
2. POST /token           → receive JWT access token
3. Add to requests       → Authorization: Bearer <token>
4. Token expires in      → 30 minutes
```

In Swagger UI, click the **Authorize** button at the top right and paste your token.

---

## Search Query Parameters

```
GET /books/search/?rating=5
GET /books/search/?author=martin
GET /books/search/?rating=4&limit=5
```

---
