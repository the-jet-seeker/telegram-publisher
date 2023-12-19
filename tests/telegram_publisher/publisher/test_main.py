from telegram_publisher.models import Trip
from telegram_publisher.publisher import main
from telegram_publisher.schemas import Trips, TripsGroup


async def test_main_nothing_found(mocker):
    mocker.patch('telegram_publisher.publisher.get_top_trips', return_value=Trips(
        groups=[],
    ))

    res = await main()

    assert res.trips_published == 0
    assert res.is_success is False


async def test_main_success(mocker, trip_first: Trip, trip_second: Trip):
    mocker.patch('telegram_publisher.publisher.get_top_trips', return_value=Trips(
        groups=[
            TripsGroup(destination_code='BCN', trips=[trip_first, trip_second]),
        ],
    ))

    res = await main()

    assert res.trips_published == 2
    assert res.is_success is True
