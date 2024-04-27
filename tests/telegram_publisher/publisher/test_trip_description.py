from telegram_publisher.models import Trip
from telegram_publisher.publisher import _trip_description


def test_trip_description(trip_first: Trip):
    res = _trip_description(trip_first)

    assert res == [
        '*220 CZK*',
        '🛫 Sun, Jan 1, 04:00 AM Norvegian Air shuttle',
        '🛬 Mon, Jan 2, 12:00 PM Norvegian Air shuttle',
        'approx cost for 1 day\\(s\\):',
        '🏠 3100 CZK   ☕️ 1900 CZK',
        '',
    ]
