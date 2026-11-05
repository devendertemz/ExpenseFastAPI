# ExpenseFastAPI

A REST API for tracking personal expenses, built with **FastAPI**, **SQLAlchemy** and **SQLite**.
It supports full CRUD for expenses and users, title search, argon2 password hashing, and JWT-based login.

## Features

- Create, read, update, delete and search expenses
- User registration with unique username / email checks
- Passwords hashed with **argon2** (never returned in responses)
- Login endpoint that returns a **JWT access token** (HS256, 30-minute expiry)
- Request validation with **Pydantic v2** (e.g. amount must be > 0, valid email format)
- Consistent `{status, message, data}` response envelope
- Interactive API docs (Swagger UI and ReDoc) generated automatically

## Tech stack

| Layer            | Library                            |
| ---------------- | ---------------------------------- |
| Web framework    | FastAPI (+ Uvicorn)                |
| ORM / database   | SQLAlchemy 2.x, SQLite             |
| Validation       | Pydantic v2, email-validator       |
| Password hashing | argon2-cffi                        |
| JWT              | python-jose                        |

## Project structure

```
ExpenseFastAPI/
├── app/
│   ├── main.py                  # App entry point; creates tables and registers routers
│   ├── core/
│   │   ├── db.py                # Engine, session factory, get_db dependency
│   │   └── jwt_helper.py        # Create / verify JWT access tokens
│   ├── models/
│   │   ├── expense_model.py     # Expense table
│   │   └── user_model.py        # User table + password verification
│   ├── schemas/
│   │   ├── api_response.py      # Standard response envelope
│   │   ├── experse_schemas.py   # Expense request/response DTOs
│   │   └── user_schemas.py      # User and login DTOs
│   └── routers/
│       ├── auth.py              # /auth   - login
│       ├── expense_route.py     # /expenses
│       └── user_route.py        # /users
├── requirements.txt
└── README.md
```

## Getting started

**Prerequisites:** Python 3.10 or newer.

1. **Clone the repository**

   ```bash
   git clone https://github.com/devendertemz/ExpenseFastAPI.git
   cd ExpenseFastAPI
   ```

2. **Create and activate a virtual environment**

   ```bash
   python -m venv venv

   # Windows (PowerShell)
   venv\Scripts\Activate.ps1

   # macOS / Linux
   source venv/bin/activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Run the server** (from the project root)

   ```bash
   uvicorn app.main:app --reload
   ```

   The API is now available at `http://127.0.0.1:8000`.
   On first start, a SQLite database file `expense.db` is created in the project root with the `users` and `expenses` tables.

5. **Open the docs**

   - Swagger UI: <http://127.0.0.1:8000/docs>
   - ReDoc: <http://127.0.0.1:8000/redoc>

## API reference

### Health

| Method | Path | Description          |
| ------ | ---- | -------------------- |
| GET    | `/`  | Returns `{"Hello": "World"}` |

### Users — `/users`

| Method | Path               | Description                                              |
| ------ | ------------------ | -------------------------------------------------------- |
| POST   | `/users/`          | Register a user (`409` if username or email already exists) |
| GET    | `/users/`          | List all users                                           |
| GET    | `/users/{user_id}` | Get a user by ID                                         |
| PUT    | `/users/{user_id}` | Partially update a user (only fields you send change)    |
| DELETE | `/users/{user_id}` | Delete a user                                            |

### Authentication — `/auth`

| Method | Path     | Description                                         |
| ------ | -------- | --------------------------------------------------- |
| POST   | `/auth/` | Log in with email + password; returns a JWT and the user |

### Expenses — `/expenses`

| Method | Path                            | Description                              |
| ------ | ------------------------------- | ---------------------------------------- |
| POST   | `/expenses/`                    | Create an expense                        |
| GET    | `/expenses/`                    | List all expenses                        |
| GET    | `/expenses/{expense_id}`        | Get an expense by ID                     |
| PUT    | `/expenses/{expense_id}`        | Replace an expense (all fields required) |
| DELETE | `/expenses/{expense_id}`        | Delete an expense                        |
| GET    | `/expenses/search/?title=<text>`| Case-insensitive search by title         |

> **Note:** the search path needs the trailing slash (`/expenses/search/`). Without it, the request is matched as `/expenses/{expense_id}` and returns `422`.

## Usage examples

### Register a user

```bash
curl -X POST http://127.0.0.1:8000/users/ \
  -H "Content-Type: application/json" \
  -d '{"username": "alice", "email": "alice@example.com", "password": "secret123"}'
```

Validation: `username` 3–50 chars, valid `email`, `password` 6–100 chars.

### Log in

```bash
curl -X POST http://127.0.0.1:8000/auth/ \
  -H "Content-Type: application/json" \
  -d '{"email": "alice@example.com", "password": "secret123"}'
```

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": 1,
    "username": "alice",
    "email": "alice@example.com",
    "created_at": "2026-11-05T13:25:03.337495"
  }
}
```

A wrong email or password returns `401 {"detail": "Invalid email or password"}`.

### Create an expense

```bash
curl -X POST http://127.0.0.1:8000/expenses/ \
  -H "Content-Type: application/json" \
  -d '{"title": "Groceries", "amount": 45.5, "description": "Weekly shopping", "show": true}'
```

```json
{
  "status": "success",
  "message": "Expense created successfully",
  "data": {
    "expense": {
      "id": 1,
      "title": "Groceries",
      "amount": 45.5,
      "description": "Weekly shopping",
      "show": true,
      "created_at": "2026-11-05T13:25:03.140696"
    }
  }
}
```

Validation: `title` 2–100 chars, `amount` > 0, `description` up to 200 chars, `show` defaults to `true`.

### Search expenses

```bash
curl "http://127.0.0.1:8000/expenses/search/?title=groc"
```

## Response format

All `/users` and `/expenses` endpoints wrap their result in the same envelope:

```json
{
  "status": "success",
  "message": "Human-readable message",
  "data": { }
}
```

Errors use FastAPI's default shape, e.g. `404 {"detail": "Expense not found"}`, or `422` with field-level details for validation failures.

## Configuration notes

- **Database:** `sqlite:///./expense.db`, set in `app/core/db.py`. The file is git-ignored and recreated automatically if missing.
- **JWT settings:** the secret key, algorithm and expiry are defined at the top of `app/core/jwt_helper.py`. The secret key is a development placeholder — **replace it (ideally load it from an environment variable) before deploying anywhere public.**

## Current limitations / roadmap

- The JWT returned by `/auth/` is not yet required by any endpoint — expense and user routes are currently open.
- Expenses are not linked to users; every client sees all expenses.
- Tables are created with `Base.metadata.create_all`, so schema changes need the DB file deleted (no migrations yet — Alembic would be the next step).
- No automated test suite yet.
