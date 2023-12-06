"""Database models."""

from pony.orm import Database, PrimaryKey

from telegram_publisher.settings import app_settings

db = Database()


class Trip(db.Entity):  # type: ignore
    """Trip table model."""

    id = PrimaryKey(int, auto=True)


db.bind(
    provider='postgres',
    user=app_settings.DATABASE_USER,
    password=app_settings.DATABASE_PASSWORD,
    host=app_settings.DATABASE_HOST,
    database=app_settings.DATABASE_NAME,
    port=app_settings.DATABASE_PORT,
)
db.generate_mapping()
