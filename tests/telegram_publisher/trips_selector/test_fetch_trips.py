import pendulum

from telegram_publisher.models import Trip
from telegram_publisher.trips_selector import _fetch_trips


def test_fetch_trips_smoke(trip_first: Trip, trip_second: Trip):
    result = _fetch_trips(
        trip_first.outbound_airport,
        trip_first.start_date,
        trip_second.end_date,
    )
    print(result)
    assert len(result) == 2
    assert {trip.id for trip in result} == {trip_first.id, trip_second.id}


def test_fetch_trips_nothing_found():
    result = _fetch_trips(
        'ZZZ',
        pendulum.today().naive(),
        pendulum.today().naive(),
    )

    assert len(result) == 0
