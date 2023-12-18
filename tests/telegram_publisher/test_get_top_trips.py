import datetime

from pony.orm import db_session

from telegram_publisher.models import Trip
from telegram_publisher.publisher import _get_top_trips


def test_get_top_trips_date_selection():
    with db_session:
        trip = Trip()

    res = _get_top_trips()

    assert res.weekend_start_date_utc >= datetime.datetime.utcnow()
