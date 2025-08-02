# Backend Assignment 2

## 📄 Assignment Goal

Implement a RESTful API for an Employee Management System using Python (FastAPI is preferred).  
The goal is to demonstrate your ability to design and implement a backend API with clean architecture, proper validation, and good documentation.

---

## ✅ Requirements

You are required to implement:

### 1. CRUD APIs for Employee

Each employee has:

- `id` (auto increment)
- `full_name`
- `email` (unique)
- `phone_number`
- `join_date`
- `job_title`
- `department`
- `salary`

### 2. Search & filter employee list

Allow filtering with:

- `department`
- `job_title`
- `date range of join_date`
- Partial match for `full_name`

### 3. Sort employee list

Allow sorting by:

- `full_name`
- `join_date`
- `salary`

Sorting should support both ASC & DESC orders.

### 4. Pagination

Support pagination with `limit` and `offset` query parameters.

---

## 📚 Optional Bonus

- Use of **Docker** to run the application
- **Unit tests**
- Proper **schema validation** using Pydantic
- **Database migrations** (with Alembic or similar)
- API documentation (Swagger UI is built-in with FastAPI)

---

## 🧪 Technical Requirements

- Language: **Python 3.9+**
- Framework: **FastAPI** (or Flask if preferred)
- DB: **PostgreSQL** or **SQLite** (for simplicity)
- ORM: **SQLAlchemy** or **Tortoise ORM**
- Structure: Follow best practices with proper **project structure**, **models**, **services**, **routers**, etc.

---

## 🚀 How to Submit

- Push your code to a **public GitHub repository**
- Include a **README** with instructions on:
  - How to run your project
  - How to use/test the API (example curl or Postman)
  - Any design decisions or assumptions

---

## 🧠 Evaluation Criteria

- Code quality and readability
- API design and validation
- Clean architecture and separation of concerns
- Correctness and completeness of features
- Use of best practices and tools (e.g., linting, typing)
- Documentation and ease of use

---

## 📝 Notes

- Do not over-engineer. Keep it simple, but clean.
- You can use a simple in-memory database or SQLite for quick setup.
- Focus on showcasing your understanding of backend design.
