# DATABASE

MySQL

## Create network
```
docker create network omnihr-net
```
## Create db
* Start DB containers,  docker-compose.db.yml is put in ./miscellaneous

```
docker compose -f docker-compose.db.yml up -d
```
* Init table: `./miscellaneous/db_create.sql`
* Add test records to reference tables: `./miscellaneous/seed_reference_table.sql`
* Add records to employee table: 
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
