from telegram_publisher.models import Trip
from telegram_publisher.publisher import _publish
from telegram_publisher.schemas import TripsGroup


async def test_publish_smoke(trip_first: Trip, trip_second: Trip):
    trips_group = TripsGroup(
        destination_code='BOD',
        trips=[trip_first, trip_second],
    )

    res = await _publish([trips_group])

    assert res == 2
