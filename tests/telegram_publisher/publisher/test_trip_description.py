from telegram_publisher.models import Trip
from telegram_publisher.message_presenter import _trip_description


def test_trip_description(trip_first: Trip):
    res = _trip_description(trip_first)

    assert res == [
        '*220 Kč*',
        '► Sun, Jan 1, 04:00 Norvegian Air shuttle',
        '◄ Mon, Jan 2, 12:00 Norvegian Air shuttle',
        '🏠 3100 Kč   ☕️ 1900 Kč',
        '',
    ]
