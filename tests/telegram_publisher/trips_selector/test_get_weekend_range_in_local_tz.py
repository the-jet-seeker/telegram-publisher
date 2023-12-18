import pendulum.day

from telegram_publisher.trips_selector import get_weekend_range_in_local_tz


def test_get_weekend_range_in_local_tz_smoke():
    response = get_weekend_range_in_local_tz()

    assert len(response) == 2
    assert response[0] < response[1]
    assert response[0].hour > 0
    assert response[0].day_of_week == pendulum.day.WeekDay.FRIDAY
    assert response[1].hour <= 24
    assert response[1].hour > 0
    assert response[1].day_of_week == pendulum.day.WeekDay.MONDAY
