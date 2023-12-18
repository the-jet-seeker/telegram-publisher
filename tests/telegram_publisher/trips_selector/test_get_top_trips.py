from decimal import Decimal

from telegram_publisher.trips_selector import get_top_trips


def test_get_top_trips_nothing_found(mocker):
    mocker.patch('telegram_publisher.trips_selector._fetch_trips', return_value=[])

    res = get_top_trips(top_n=100500)

    assert len(res.groups) == 0


def test_get_top_trips_sort_by_total_cost(mocker):
    mocker.patch('telegram_publisher.trips_selector._fetch_trips', return_value=[
        dict(
            id=1,
            outbound_cost=Decimal(2),
            return_airport='BCN',
            return_cost=Decimal(1),
        ),
        dict(
            id=2,
            outbound_cost=Decimal(1),
            return_airport='BCN',
            return_cost=Decimal(3),
        ),
        dict(
            id=3,
            outbound_cost=Decimal(1),
            return_airport='BCN',
            return_cost=Decimal(1),
        ),
    ])

    res = get_top_trips(top_n=100500)

    assert len(res.groups) == 1
    assert res.groups[0].destination_code == 'BCN'
    assert res.groups[0].trips[0]['id'] == 3
    assert res.groups[0].trips[1]['id'] == 1
    assert res.groups[0].trips[2]['id'] == 2


def test_get_top_trips_group_by_destination(mocker):
    mocker.patch('telegram_publisher.trips_selector._fetch_trips', return_value=[
        dict(
            id=1,
            outbound_cost=Decimal(2),
            return_airport='BCN',
            return_cost=Decimal(1),
        ),
        dict(
            id=2,
            outbound_cost=Decimal(1),
            return_airport='AMS',
            return_cost=Decimal(0),
        ),
        dict(
            id=3,
            outbound_cost=Decimal(1),
            return_airport='BCN',
            return_cost=Decimal(1),
        ),
    ])

    res = get_top_trips(top_n=100500)

    assert len(res.groups) == 2
    assert res.groups[0].destination_code == 'AMS'
    assert res.groups[1].destination_code == 'BCN'
    assert res.groups[0].trips[0]['id'] == 2
    assert res.groups[1].trips[0]['id'] == 3
    assert res.groups[1].trips[1]['id'] == 1


def test_get_top_trips_limit(mocker):
    mocker.patch('telegram_publisher.trips_selector._fetch_trips', return_value=[
        dict(
            id=1,
            outbound_cost=Decimal(3),
            return_airport='BCN',
            return_cost=Decimal(0),
        ),
        dict(
            id=2,
            outbound_cost=Decimal(10),
            return_airport='ZZZ',
            return_cost=Decimal(0),
        ),
        dict(
            id=3,
            outbound_cost=Decimal(2),
            return_airport='BCN',
            return_cost=Decimal(0),
        ),
        dict(
            id=4,
            outbound_cost=Decimal(1),
            return_airport='ZZZ',
            return_cost=Decimal(0),
        ),
    ])

    res = get_top_trips(top_n=3)

    assert len(res.groups) == 2
    assert res.groups[0].destination_code == 'ZZZ'
    assert res.groups[1].destination_code == 'BCN'
    assert len(res.groups[0].trips) == 1
    assert len(res.groups[1].trips) == 2
    assert res.groups[0].trips[0]['id'] == 4
