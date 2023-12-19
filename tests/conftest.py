import asyncio
import datetime
from decimal import Decimal

import pendulum
import pytest

from telegram_publisher.models import Session, Trip


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def trip_first() -> Trip:
    with Session() as session:
        trip = Trip(
            start_date=pendulum.naive(2023, 1, 1, 4, 0, 0, 0),
            end_date=pendulum.naive(2023, 1, 2, 12, 0, 0, 0),
            currency='CZK',
            outbound_cost=Decimal(120),
            outbound_airport='PRG',
            outbound_airline='TEST airlines',
            outbound_fly_number='TEST321',
            return_cost=Decimal(100),
            return_airport='BCN',
            return_airline='TEST airlines',
            return_fly_number='TEST123',
        )
        session.add(trip)
        session.commit()

        yield trip

        session.delete(trip)
        session.commit()


@pytest.fixture
def trip_second() -> Trip:
    with Session() as session:
        trip = Trip(
            start_date=datetime.datetime(2023, 1, 2, 4, 0, 0, 0),
            end_date=datetime.datetime(2023, 1, 3, 11, 0, 0, 0),
            currency='CZK',

            outbound_cost=Decimal(120),
            outbound_airport='PRG',
            outbound_airline='TEST airlines',
            outbound_fly_number='TEST321',

            return_cost=Decimal(100),
            return_airport='BCN',
            return_airline='TEST airlines',
            return_fly_number='TEST123',
        )
        session.add(trip)
        session.commit()

        yield trip

        session.delete(trip)
        session.commit()
