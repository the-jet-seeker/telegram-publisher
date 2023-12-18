from unittest.mock import Mock

from telegram_publisher.publisher import _publish
from telegram_publisher.schemas import TripsGroup


async def test_publish_smoke():
    trips_group = TripsGroup(
        destination_code='BCN',
        trips=[Mock(id=0), Mock(id=1)],
    )

    res = await _publish([trips_group], 'Publisher unittests')

    assert res == 2
