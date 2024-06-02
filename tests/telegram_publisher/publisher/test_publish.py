from telegram_publisher.models import Trip
from telegram_publisher.publisher import _publish
from telegram_publisher.schemas import TripsGroup
from telegram_publisher.trips_selector import get_weekend_range_in_local_tz


async def test_publish_smoke(trip_first: Trip, trip_second: Trip):
    weekend_range = get_weekend_range_in_local_tz()
    trips_group = TripsGroup(
        destination_code='BOD',
        trips=[trip_second, trip_first],
    )

    res = await _publish([trips_group], weekend_range)

    assert res == 2
