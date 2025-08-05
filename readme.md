# 🧠 OmniHR — Employee Search Microservice

A containerized, high-performance, FastAPI-based microservice that powers employee directory search for HR platforms.

---

## 📦 Features

- 🔍 Search API with advanced filters
- 🧩 Dynamic column configuration (org-level visibility)
- 🛡️ Built-in rate limiting (thread-safe, no 3rd party lib)
- ⚡ Optimized for large-scale datasets
- ✅ Fully unit tested
- 🐳 Dockerized for easy deployment
- 📄 OpenAPI support via `/docs`

---

## ⚙️ Tech Stack

- Language: Python 3.11+
- Framework: FastAPI
- DB: MySQL
- ORM: SQLAlchemy
- Test: Pytest
- Container: Docker, Docker Compose

---

## 🚀 Getting Started

### 1. Clone Repository

```bash
git clone https://github.com/truongthuanr/omnihr.git
cd omnihr
```

### 2. Create Docker Network

```bash
docker network create omnihr-net
```

### 3. Start Database

```bash
docker compose -f ./miscellaneous/docker-compose.db.yml up -d
```

### 4. Initialize Database Schema

```bash
mysql -h 127.0.0.1 -P 3306 -u root -p omnihr < ./miscellaneous/db_create.sql
```

### 5. Seed Reference Data

```bash
mysql -h 127.0.0.1 -P 3306 -u root -p omnihr < ./miscellaneous/seed_reference_table.sql
```

### 6. (Optional) Seed Sample Employees

```bash
mysql -h 127.0.0.1 -P 3306 -u root -p omnihr < ./miscellaneous/seed_employees.sql
```

---

## 🖥️ Run the Service

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Access API docs: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 🧪 Run Tests

```bash
pytest tests/
```

Ensure DB is up and seeded before running tests.

---

## 🛠️ Configuration

All configuration is JSON-based and loaded via `CONFIG_PATH` (default: `/app/config/config.json`).

```json
{
  "rate_limit": {
    "max_requests": 10,
    "window_seconds": 60,
    "max_global_requests": 1000
  },
  "columns": {
    "id": true,
    "first_name": true,
    "last_name": true,
    "contact": true,
    "department": true,
    "position": true,
    "location": true,
    "company": true
  }
}
```

Override with:

```bash
export CONFIG_PATH=/custom/path/to/config.json
```

Config is cached in memory with default TTL = 60 seconds.

---

## 🔧 Dynamic Column Configuration

Organizations can customize which fields appear in search result responses.

- Configurable via JSON
- Controlled by `columns` flags (`true`/`false`)
- Supports fallback to default if no config provided

### 📤 Sample API Response

```json
[
  {
    "id": 2348,
    "first_name": "Dorothy",
    "last_name": "Bentley",
    "contact": "dorothy.bentley@example.com",
    "department": "Engineering",
    "position": "UX/UI Designer",
    "location": "United States",
    "company": "Zorg Industries"
  }
]
```

---

## 🛡️ Rate Limiting

Custom implementation of **Fixed Window Limiting** using `threading.Lock`.

### ✅ Supported Features

- Per-IP rate limit
- Optional global limit
- Thread-safe (using Lock)
- Configurable via JSON
- `"anonymous"` fallback for unknown IPs

### ⚙️ How It Works

- Count requests by IP in fixed time windows
- Reject (`429`) if limit is exceeded
- Decorator-based integration with routers

### 🧩 FastAPI Integration

```python
from app.rate_limiting.rate_limiter import rate_limited
from app.rate_limiting.fixed_window import FixedWindowLimiter

limiter = FixedWindowLimiter()

@router.get("/employees/search")
@rate_limited(limiter)
async def search_employees(...):
    ...
```

---

## 📬 API Example

**Endpoint**: `/employees/search`

**Query Params**:
- `status_id`
- `location_id`
- `department_id`
- `position_id`
- `company_id`
- `page`
- `size`

**Sample Request:**

```bash
curl -X GET "http://localhost:8000/employees/search?status_id=1&location_id=1&page=1&size=20"
```

**Sample Response**:

```json
[
  {
    "id": 4713,
    "first_name": "Abigail",
    "last_name": "Cuevas",
    "contact": "abigail.cuevas@example.com",
    "department": "Engineering",
    "position": "Finance Analyst",
    "location": "United States",
    "company": "Zenith AI"
  }
]
```

---

## 📂 Project Structure

```
omnihr/
├── app/
│   ├── main.py
│   ├── api/
│   ├── models/
│   ├── db/
│   ├── config/
│   ├── rate_limiting/
│   └── ...
├── tests/
├── miscellaneous/
│   ├── docker-compose.db.yml
│   ├── db_create.sql
│   ├── seed_reference_table.sql
│   └── seed_employees.sql
└── README.md
```

---
<!-- 
## ✅ Assignment Compliance

- [x] Search API implemented (no CRUD)
- [x] Dynamic columns via config
- [x] Rate limiting implemented manually (no external libs)
- [x] No data leakage across organizations
- [x] Unit tests included
- [x] OpenAPI docs available
- [x] Fully containerized
 -->
