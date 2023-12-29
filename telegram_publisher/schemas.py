"""App schemas."""

from dataclasses import dataclass

import pendulum

from telegram_publisher.models import Trip


@dataclass
class PublisherResponse:
    """Task response schema."""

    is_success: bool
    date_range: tuple[pendulum.DateTime, pendulum.DateTime]
    trips_published: int = 0


@dataclass
class TripsGroup:
    """Group of trips by destination."""

    trips: list[Trip]
    destination_code: str


@dataclass
class Trips:
    """Possible trips result schema."""

    groups: list[TripsGroup]
