"""Database models."""
from datetime import datetime
from decimal import Decimal

from pony.orm import Database, PrimaryKey, Required

from telegram_publisher.settings import app_settings

db = Database()


class Trip(db.Entity):  # type: ignore
    """Trip table model."""

    id = PrimaryKey(int, auto=True)
    start_date = Required(datetime)  # local home airport time
    end_date = Required(datetime)  # local home airport time
    currency = Required(str)

    outbound_cost = Required(Decimal)
    outbound_airport = Required(str)
    outbound_airline = Required(str)
    outbound_fly_number = Required(str)

    return_cost = Required(Decimal)
    return_airport = Required(str)
    return_airline = Required(str)
    return_fly_number = Required(str)


db.bind(
    provider='postgres',
    user=app_settings.DATABASE_USER,
    password=app_settings.DATABASE_PASSWORD,
    host=app_settings.DATABASE_HOST,
    database=app_settings.DATABASE_NAME,
    port=app_settings.DATABASE_PORT,
)
db.generate_mapping()
