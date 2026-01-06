# 🧠 OmniHR — Employee Search Microservice

FastAPI microservice for employee directory search, built for multi-tenant HR platforms.

---

## 📦 Features
- 🔍 Search API with advanced filters
- 🧩 Dynamic column configuration per organization
- 🔎 Strict Pydantic response validation to prevent data leakage
- 🛡️ Organization-level access control via API keys
- 🔐 Built-in rate limiting (thread-safe, no third-party lib)
- ⚡ Designed for large datasets with pagination and indexing
- ✅ Unit tests included
- 🐳 Dockerized; OpenAPI docs at `/docs`

---

## ⚙️ Tech Stack
- Language: Python 3.11+
- Framework: FastAPI
- DB: MySQL
- ORM: SQLAlchemy
- Tests: Pytest
- Container: Docker, Docker Compose

---

## 🚀 Getting Started

### Quick Request Example\
###### Request
```bash
curl -X 'GET' \
  'http://localhost:8000/employees/search?status_id=1&status_id=2&location_id=3&department_id=4&position_id=2&page=1&size=20' \
  -H 'accept: application/json' \
  -H 'X-ORG-KEY: key-omnihr-001'
```
###### Response
```bash
{
  "page": 1,
  "size": 20,
  "total": 21,
  "total_pages": 2,
  "data": [
    {
      "id": 17584,
      "first_name": "Priscilla",
      "last_name": "Stevenson",
      "contact": "priscilla.stevenson@example.com",
      "department": "Customer Support",
      "location": "United Kingdom",
      "position": "Backend Developer",
      "status": "active",
      "company": "Prestige Worldwide"
    },
    ...
}
```

### Deploy
1) Clone
```bash
git clone https://github.com/truongthuanr/omnihr.git
cd omnihr
```
2) Database
```bash
docker compose up -d omnihr-db
# schema + sample data (employees.sql is large)
docker compose exec -T omnihr-db mysql -uroot -proot omnihr-db < miscellaneous/db_create.sql
docker compose exec -T omnihr-db mysql -uroot -proot omnihr-db < miscellaneous/seed_reference_tables.sql
docker compose exec -T omnihr-db mysql -uroot -proot omnihr-db < miscellaneous/employees.sql
```
3) Service
```bash
docker compose up -d omnihr-service
```
- Swagger UI: http://localhost:8000/docs  
- Sample request (seeded key):
```bash
curl -X 'GET' \
  'http://localhost:8000/employees/search?status_id=1&status_id=2&location_id=3&department_id=4&position_id=2&page=1&size=20' \
  -H 'accept: application/json' \
  -H 'X-ORG-KEY: key-omnihr-001'
```

---

## Feature Details
### Search API
- Optional filters: name, status_id, location_id, company_id, department_id, position_id (see `EmployeeSearchParams`).
- Database queries executed based on provided filters.

### Organization Scoping
- Search is scoped by organization derived from `X-ORG-KEY` to prevent cross-tenant data leakage.
- Organization filtering is enforced at query time.

### Dynamic Column Responses
- Configurable per organization; fallback to defaults in `omnihr-service/configs/customconfig.json`.

Default config example:
```bash
"default": {
    "columns": {
      "id": true,
      "first_name": true,
      "last_name": true,
      "status": true,
      "contact": true,
      "department": true,
      "position": true,
      "location": true,
      "company": true
    }
    ...
}
```

Org-specific example:
```bash
"orgs": {
  "1": {
    "columns": {
      "id": false,
      "first_name": true,
      "last_name": true,
      "status": false,
      "contact": false,
      "department": true,
      "position": true,
      "location": true,
      "company": false
    }
}
```

### Performance
- Pagination with size limits to avoid large scans and payloads.
- DB indexes on search filters (`status_id`, `location_id`, `company_id`, `department_id`, `position_id`, `last_name`, `first_name`) to speed lookups.
- Dynamic columns keep responses lean per tenant config.
- Rate limiting protects the service during spikes (fixed-window per-IP/global).
- Performance test (`omnihr-service/tests/test_performance.py`) exercises `/employees/search` with varied filters; local runs average ~53 ms (max ~156 ms) under current thresholds.

### Rate Limiting
- Decorator-based, fixed-window strategy for per-IP and global limits.
- Configuration in `omnihr-service/configs/customconfig.json`.

Example:
```bash
"rate_limit": {
  "max_requests": 10,
  "window_seconds": 60,
  "max_global_requests": 1000
}
```

---

## 🧪 Run Tests
```bash
pytest tests/
```
Ensure DB is up and seeded before running tests.

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
