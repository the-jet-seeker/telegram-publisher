from unittest.mock import Mock

from telegram_publisher.publisher import main
from telegram_publisher.schemas import Trips, TripsGroup


async def test_main_nothing_found(mocker):
    mocker.patch('telegram_publisher.publisher.get_top_trips', return_value=Trips(
        groups=[],
    ))

    res = await main()

    assert res.trips_published == 0
    assert res.is_success is False


async def test_main_success(mocker):
    mocker.patch('telegram_publisher.publisher.get_top_trips', return_value=Trips(
        groups=[
            TripsGroup(destination_code='BCN', trips=[Mock(id=0), Mock(id=1)]),
        ],
    ))

    res = await main()

    assert res.trips_published == 2
    assert res.is_success is True
