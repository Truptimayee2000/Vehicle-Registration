import json
from datetime import datetime
from sqlalchemy import text
from dbconfig import engine


def clean_value(value):
    """Convert numeric strings with commas to int, empty strings to None."""
    if value == "" or value is None:
        return None
    if isinstance(value, str) and value.replace(",", "").isdigit():
        return int(value.replace(",", ""))
    return value


def add_metadata(record):
    """Add default metadata fields if they don't exist."""
    now = datetime.now()
    defaults = {
        "created_on": now,
        "created_by": "system",
        "updated_on": now,
        "updated_by": "system",
        "is_active": True
    }
    for k, v in defaults.items():
        record.setdefault(k, v)
    return record


def insert_data(conn, table_name, data, field_mapping):
    """Generic insert function."""
    for record in data:
        record = {k: clean_value(v) for k, v in record.items()}
        record = add_metadata(record)

        record = {k: record[k] for k in field_mapping}

        fields = ", ".join(field_mapping)
        placeholders = ", ".join(f":{f}" for f in field_mapping)

        conn.execute(
            text(f"INSERT INTO {table_name} ({fields}) VALUES ({placeholders})"),
            record
        )


def load_initial_data():
    with engine.connect() as conn:
        manufacture_count = conn.execute(text("SELECT COUNT(*) FROM manufacture")).scalar()
        category_count = conn.execute(text("SELECT COUNT(*) FROM vehicle_category")).scalar()

        if manufacture_count == 0:
            with open("../data/manufacture.json", encoding="utf-8") as f:
                manufacture_data = json.load(f)

            manufacture_fields = [
                "manufacturer", "year", "jan", "feb", "mar", "apr", "may", "jun", "jul", "aug",
                "sep", "oct", "nov", "dec", "total",
                "created_on", "created_by", "updated_on", "updated_by", "is_active"
            ]
            insert_data(conn, "manufacture", manufacture_data, manufacture_fields)
            print("Manufacture data inserted.")

        if category_count == 0:
            with open("../data/vehicle_type.json", encoding="utf-8") as f:
                category_data = json.load(f)

            category_fields = [
                "vehicle_category", "year", "jan", "feb", "mar", "apr", "may", "jun", "jul", "aug",
                "sep", "oct", "nov", "dec", "total",
                "created_on", "created_by", "updated_on", "updated_by", "is_active"
            ]
            insert_data(conn, "vehicle_category", category_data, category_fields)
            print("Vehicle category data inserted.")

        conn.commit()
