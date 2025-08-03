import random
import argparse
from faker import Faker

faker = Faker()

# Configurable ranges for foreign key IDs
DEPARTMENT_COUNT = 15
POSITION_COUNT = 20
LOCATION_COUNT = 50
STATUS_COUNT = 3
COMPANY_COUNT = 98


def sql_escape(value: str) -> str:
    return value.replace("'", "''")


def generate_names(count):
    firstnames = list({faker.first_name() for _ in range(count * 2)})[:count]
    lastnames = list({faker.last_name() for _ in range(count * 2)})[:count]
    return firstnames, lastnames


def generate_employees(n, firstnames, lastnames):
    for _ in range(n):
        fname = random.choice(firstnames)
        lname = random.choice(lastnames)
        email = f"{fname.lower()}.{lname.lower()}@example.com"

        yield (
            sql_escape(fname),
            sql_escape(lname),
            sql_escape(email),
            random.randint(1, DEPARTMENT_COUNT),
            random.randint(1, POSITION_COUNT),
            random.randint(1, LOCATION_COUNT),
            random.randint(1, STATUS_COUNT),
            random.randint(1, COMPANY_COUNT)
        )


def export_sql(filename: str, employees, batch_size: int):
    with open(filename, "w", encoding="utf-8") as f:
        batch = []
        for idx, row in enumerate(employees, start=1):
            values = ", ".join(f"'{v}'" if isinstance(v, str) else str(v) for v in row)
            batch.append(f"({values})")
            if idx % batch_size == 0:
                f.write("INSERT INTO employees (first_name, last_name, contact, department_id, position_id, location_id, status_id, company_id) VALUES\n")
                f.write(",\n".join(batch))
                f.write(";\n\n")
                batch.clear()

        if batch:
            f.write("INSERT INTO employees (first_name, last_name, contact, department_id, position_id, location_id, status_id, company_id) VALUES\n")
            f.write(",\n".join(batch))
            f.write(";\n")


def main():
    parser = argparse.ArgumentParser(description="Generate fake employee data and export to .sql")
    parser.add_argument("--count", type=int, default=100000, help="Number of employee records to generate")
    parser.add_argument("--out", type=str, default="employees.sql", help="Output .sql file path")
    parser.add_argument("--names", type=int, default=10000, help="Number of distinct first/last names")
    parser.add_argument("--batch", type=int, default=1000, help="Rows per SQL INSERT statement")
    args = parser.parse_args()

    firstnames, lastnames = generate_names(args.names)
    employees = generate_employees(args.count, firstnames, lastnames)
    export_sql(args.out, employees, args.batch)
    print(f"✅ Generated {args.count} employees to {args.out} in batches of {args.batch}")


if __name__ == "__main__":
    main()
