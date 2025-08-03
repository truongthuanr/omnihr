# Database

MySQL

## Create network
docker create network omnihr-net

## Create db
* Start DB containers,  docker-compose.db.yml is put in ./miscellaneous

```
docker compose -f docker-compose.db.yml up -d
```
* Init table: `./miscellaneous/db_create.sql`
* Add test records to reference tables: `./miscellaneous/seed_reference_table.sql`
* Add records to employee table: 