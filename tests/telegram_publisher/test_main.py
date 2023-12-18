from unittest.mock import Mock

import pendulum

from telegram_publisher.publisher import main
from telegram_publisher.schemas import Trips, TripsGroup


async def test_main_nothing_found(mocker):
    mocker.patch('telegram_publisher.publisher._get_top_trips', return_value=Trips(
        groups=[],
        weekend_start_date_utc=pendulum.now(),
    ))

    res = await main()

    assert res.trips_published == 0
    assert res.is_success is False


async def test_main_success(mocker):
    mocker.patch('telegram_publisher.publisher._get_top_trips', return_value=Trips(
        groups=[
            TripsGroup(destination_code='BCN', trips=[Mock(id=0), Mock(id=1)]),
        ],
        weekend_start_date_utc=pendulum.now(),
    ))

    res = await main()

    assert res.trips_published == 2
    assert res.is_success is True
