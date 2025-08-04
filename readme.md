## 🗄️ Database Setup

This service uses **MySQL** as the database engine.

### 1. Create Docker Network

Create a dedicated Docker network to ensure isolated container communication:

```
docker network create omnihr-net
```

### 2. Start Database Container

The MySQL service is defined in the `docker-compose.db.yml` file located in the `./miscellaneous` directory.

To start the database container:

```
docker compose -f ./miscellaneous/docker-compose.db.yml up -d
```

This will run MySQL with the proper volume, credentials, and network settings.

### 3. Initialize Database Schema

Execute the SQL script to create the required tables:

```
mysql -h 127.0.0.1 -P 3306 -u root -p omnihr < ./miscellaneous/db_create.sql
```

### 4. Seed Reference Data

Populate reference data into the lookup tables (e.g., departments, positions, locations, statuses):

```
mysql -h 127.0.0.1 -P 3306 -u root -p omnihr < ./miscellaneous/seed_reference_table.sql
```

### 5. Seed Sample Employees (Optional)

To populate the `employees` table with sample data for testing, use the following script:

```
mysql -h 127.0.0.1 -P 3306 -u root -p omnihr < ./miscellaneous/seed_employees.sql
```

> ℹ️ Replace credentials and database name (`omnihr`) accordingly if different in your setup.

***
***

# SERVICE

### 🔧 Dynamic Column Configuration

The search API supports **organization-level customization** of which employee fields should be returned in the response.

#### 📌 Feature Description

Different organizations may prefer to display different subsets of employee attributes in their search result. For example:

- Org A may require full details: `first_name`, `last_name`, `contact`, `department`, `position`, `location`, `company`
- Org B may hide sensitive fields like `contact` or `company`

This behavior is configured via a **JSON-based column config file**, which defines visible fields in the response. If no custom configuration is found, the service falls back to a default schema.

#### 🧾 Example Configuration File

`configs/customconfig.json`

```json
{
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

#### ⚙️ Implementation Notes

- The service reads this config from a path specified via the `CONFIG_PATH` environment variable.
- Configuration is **cached in memory** using a TTL mechanism to reduce I/O overhead.
- Any attribute marked `false` will be excluded from the serialized response.
- No configuration CRUD API is implemented, as per assignment constraints.

#### 📤 Example Response Based on Above Config

Request:

```
GET /employees/search?status_id=1&location_id=1&department_id=1&page=1&size=20
```

Response:

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
  },
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

Only the columns marked as `true` in `columns` will appear in the response.


## 🛡️ Rate Limiting

The system uses a **Fixed Window Limiting** algorithm to control API request frequency, helping to protect backend resources and prevent abuse.

### ✅ Supported Features

- **Per-IP limiting**: Each client IP is tracked independently.
- **Global limiting** *(optional)*: The total number of requests from all IPs within the window.
- **Fixed window strategy**: Requests are counted in fixed-length time windows (e.g., every 60 seconds).
- **Thread-safe**: Uses `threading.Lock` to ensure safety during concurrent access.
- **Fallback `"anonymous"` IP**: If `request.client.host` is unavailable, the request is attributed to `"anonymous"`.

---

### ⚙️ How It Works

1. On each request, the client IP is extracted from `request.client.host`. If not available, it is mapped to `"anonymous"`.
2. For each IP:
   - If the number of requests is below `max_requests` within `window_seconds` → accept and increment counter.
   - If the limit is exceeded → return `429 Too Many Requests`.
3. If `max_global_requests` is configured, the total count from all IPs is also checked.

---

### 🔧 Configuration

Configuration is loaded from a `config.json` file or overridden using the `CONFIG_PATH` environment variable.

Sample config structure:

```json
{
  "rate_limit": {
    "max_requests": 10,
    "window_seconds": 60,
    "max_global_requests": 1000
  }
}
```

- Default path: `/app/config/config.json`
- Override with environment variable:

```bash
export CONFIG_PATH=/path/to/custom_config.json
```

The config is cached with a default TTL of 60 seconds.

---

### 🧩 Integration with FastAPI Router

The rate limiter is applied via a decorator pattern.

**1. Initialize limiter from config:**

```python
from app.config.config import get_config
from app.rate_limiting.fixed_window import FixedWindowLimiter

# 💡 Create limiter instance (per-IP + global limit)
# Limiter's configuration will be read from CONFIG_PATH
limiter = FixedWindowLimiter()
```

**2. Apply to route using decorator:**

```python
from app.rate_limiting.rate_limiter import rate_limited

@router.get("/employees/search")
@rate_limited(rate_limiter)
async def search_employees(...):
    ...
```

