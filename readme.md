# 🧠 OmniHR — Employee Search Microservice - Overview

A containerized, high-performance, FastAPI-based microservice that powers employee directory search for HR platforms.

---

## 📦 Features

- 🔍 Search API with advanced filters
- 🧩 Dynamic column configuration (org-level visibility)
- 🔎 Strict response validation using Pydantic to prevent field-level data leakage
- 🛡️ Organization-level access control: each organization can only access its own employee data (row-level isolation)
- 🔐 Built-in rate limiting (thread-safe, no 3rd party lib)
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

### Example Usage (Request and Response)
Request:

```bash
curl -X 'GET' \
  'http://localhost:8000/employees/search?status_id=2&page=1&size=2' \
  -H 'accept: application/json' \
  -H 'X-ORG-KEY: key-workday-001'
```

Response:

```bash
{
  "page": 1,
  "size": 2,
  "total": 166473,
  "total_pages": 83237,
  "data": [
    {
      "first_name": "Christopher",
      "last_name": "Romero",
      "company": "Zion Technologies"
    },
    {
      "first_name": "Max",
      "last_name": "Frey",
      "company": "Illuminati Holdings"
    }
  ]
}
```
### Deploy

### 1. Clone Repository

```bash
git clone https://github.com/truongthuanr/omnihr.git
cd omnihr
```

### Database
- Start MySQL
```bash
docker compose up -d omnihr-db
```
- Seed schema + sample data (run from repo root; `employees.sql` is large, import may take a bit)
```bash
docker compose exec -T omnihr-db mysql -uroot -proot omnihr-db < miscellaneous/db_create.sql
docker compose exec -T omnihr-db mysql -uroot -proot omnihr-db < miscellaneous/seed_reference_tables.sql
docker compose exec -T omnihr-db mysql -uroot -proot omnihr-db < miscellaneous/employees.sql
```

### Service
- Start API (after DB is up/seeding done)
```bash
docker compose up -d omnihr-service
```
- Swagger UI: http://localhost:8000/docs
- Sample request (uses seeded key)
```bash
curl -X 'GET' \
  'http://localhost:8000/employees/search?status_id=2&page=1&size=2' \
  -H 'accept: application/json' \
  -H 'X-ORG-KEY: key-workday-001'
```

## Feature Details
### Search API
- Supports optional filters: name, status_id, location_id, company_id, department_id, and position_id (see `EmployeeSearchParams`).
- Executes database queries based on the provided filters.

### Dynamic Column Responses
- Response columns are configurable and support multi-tenant overrides.
- Configure defaults and per-organization settings in `omnihr-service\configs\customconfig.json`.

Example default config:
```bash
"default": {
    "columns": {
      "id": true,
      "first_name": true,
      "last_name": true,
      "contact": true,
      "department": true,
      "position": true,
      "location": true,
      "company": true
    },
    ...
```

Example organization-specific config:
```bash
"orgs": {
    "1": {
      "columns": {
        "id": false,
        "first_name": true,
        "last_name": true,
        "contact": false,
        "department": true,
        "position": true,
        "location": true,
        "company": false
      }
```

### Rate Limiting
- Implemented via a decorator pattern.
- Uses a fixed-window strategy for both per-IP and global limiters.
- Configuration lives in `omnihr-service\configs\customconfig.json`.

Example configuration:
```bash
    "rate_limit": {
      "max_requests": 10,
      "window_seconds": 60,
      "max_global_requests": 1000
```

---

## 🧪 Run Tests

```bash
pytest tests/
```

Ensure DB is up and seeded before running tests.

---
<!---
## 🛠️ Configuration

This service supports organization-specific column configuration, read from a JSON config file.

By default, the service reads config from a fixed path inside the container:

```
/configs/config.json
```

To provide custom configuration, mount your desired config file to this path using `docker-compose.yml`:

```yaml
services:
  omnihr-api:
    build: .
    volumes:
      - ./configs/org1_config.json:/configs/config.json
    environment:
      CONFIG_PATH: /configs/config.json
```

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

Config is cached in memory with default TTL = 60 seconds.

---

## 🔧 Dynamic Column Configuration

Organizations can customize which fields appear in search result responses.

- Configurable via JSON
- Controlled by `columns` flags (`true`/`false`)
- Supports fallback to default if no config provided

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

## 🔐 Response Validation & Data Leakage Prevention

To ensure data isolation and prevent accidental exposure of internal fields (e.g., salary, notes, internal IDs), the API response is strictly validated using a defined `EmployeeRead` Pydantic schema.

Even though the response supports **dynamic column configuration per organization**, all data is first validated against this schema before serialization. After validation, only allowed fields (as configured per org) are included in the final output using Pydantic's `.model_dump(include=...)`.

This approach ensures:

- ✅ Only whitelisted fields are returned per organization
- ✅ Fields not defined in the schema can never be leaked, even if misconfigured
- ✅ Full schema validation is still applied before serialization
- ✅ Clean separation between dynamic response logic and schema safety

---
## 🔐 Multi-Organization Isolation & API Access Control

This service is designed to support multiple organizations (multi-tenant). To prevent **data leakage between organizations**, the following mechanisms are enforced:

### ✅ API Key Based Access Control

- Each organization is issued a unique `X-ORG-KEY` (API key), stored in the `org_api_keys` table.
- All incoming API requests **must include** this key in the request header:

  ```
  X-ORG-KEY: key-omnihr-001
  ```

- The backend maps this API key to the correct `organization_id`, and enforces that all queries and data access are **restricted to that organization** only.

### ✅ Data Isolation

- All employee records are linked to an `organization_id`.
- Any attempt to query across organizations is prevented at the **query layer**, regardless of input filters.
<!-- - Fields like `internal_note` are treated as internal-only and **never exposed** in the API response. -->

---

### 🚧 Future Improvements (Authentication & Security)

This current version uses simple API key authentication for isolation.

In a production-grade system, this can be extended to:

- 🔐 Replace `X-ORG-KEY` with **JWT-based authentication**, containing `organization_id` as a claim.
- 🔄 Support OAuth2 flows or role-based access control (RBAC).
- 🔍 Add **audit logging per organization**, tracking queries and access.
- 📦 Cache API key lookups (e.g., using Redis) for performance.

---
<!---
## 📬 API Example

**Endpoint**: `/employees/search`

**Query Parameters**:

| Param            | Type     | Description                               |
|------------------|----------|-------------------------------------------|
| `name`           | string   | Filter by full name (first or last name)  |
| `status_id`      | int      | Filter by employment status               |
| `location_id`    | int      | Filter by work location                   |
| `department_id`  | int      | Filter by department                      |
| `position_id`    | int      | Filter by job position                    |
| `company_id`     | int      | Filter by company                         |
| `page`           | int      | Page number (default: 1)                  |
| `size`           | int      | Page size (default: 20, max: 100)         |

**Sample Request:**

```bash
curl -X GET "http://localhost:8000/employees/search?name=John&status_id=1&location_id=3&department_id=1&position_id=1&company_id=1&page=1&size=20"
```

> You can combine multiple filters together, e.g. search by name, location, and department.


**Sample Response**:

```json
{
    "page": 2,
    "size": 20,
    "total": 50,
    "total_pages": 3,
    "data": [
        {
            "id": 41140,
            "first_name": "Vincent",
            "last_name": "Johnson",
            "position": "UX/UI Designer",
            "company": "BLUTH Company"
        },
        ...
    ]
}
```
--->
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
