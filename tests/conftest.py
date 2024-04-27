import asyncio
import datetime
from decimal import Decimal

import pendulum
import pytest

from telegram_publisher import bot_setup
from telegram_publisher.models import Session, Trip


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session", autouse=True)
async def close_aiohttp_session():
    yield
    await bot_setup.session.close()


@pytest.fixture
def trip_first() -> Trip:
    with Session() as session:
        trip = Trip(
            start_date=pendulum.naive(2023, 1, 1, 4, 0, 0, 0),
            end_date=pendulum.naive(2023, 1, 2, 12, 0, 0, 0),
            currency='CZK',

            outbound_cost=Decimal(120),
            outbound_airport='PRG',
            outbound_airline='Norvegian Air shuttle',
            outbound_fly_number='TEST321',

            return_cost=Decimal(100),
            return_airport='BCN',
            return_airline='Norvegian Air shuttle',
            return_fly_number='TEST123',

            duration_nights=1,
            meals_amount=5,
            rent_cost=3135,
            meal_cost=380,
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
            outbound_airline='Ryanair',
            outbound_fly_number='TEST321',

            return_cost=Decimal(100),
            return_airport='BCN',
            return_airline='TEST airlines',
            return_fly_number='TEST123',

            duration_nights=1,
            meals_amount=5,
            rent_cost=3135,
            meal_cost=380,
        )
        session.add(trip)
        session.commit()

        yield trip

        session.delete(trip)
        session.commit()

@pytest.fixture
def trip_ryanair_both_ways() -> Trip:
    with Session() as session:
        trip = Trip(
            start_date=pendulum.naive(2024, 3, 9, 4, 0, 0, 0),
            end_date=pendulum.naive(2024, 3, 10, 12, 0, 0, 0),
            currency='CZK',
            outbound_cost=Decimal(120),
            outbound_airport='PRG',
            outbound_airline='Ryanair',
            outbound_fly_number='TEST321',
            return_cost=Decimal(100),
            return_airport='BLQ',
            return_airline='Ryanair',
            return_fly_number='TEST123',

            duration_nights=1,
            meals_amount=5,
            rent_cost=2486,
            meal_cost=506,
        )
        session.add(trip)
        session.commit()

        yield trip

        session.delete(trip)
        session.commit()


@pytest.fixture
def trip_easyjet_both_ways() -> Trip:
    with Session() as session:
        trip = Trip(
            start_date=pendulum.naive(2024, 4, 12, 4, 0, 0, 0),
            end_date=pendulum.naive(2024, 4, 14, 12, 0, 0, 0),
            currency='CZK',
            outbound_cost=Decimal(120),
            outbound_airport='PRG',
            outbound_airline='easyJet',
            outbound_fly_number='TEST321',
            return_cost=Decimal(100),
            return_airport='MXP',
            return_airline='easyJet',
            return_fly_number='TEST123',

            duration_nights=2,
            meals_amount=9,
            rent_cost=3623,
            meal_cost=506,
        )
        session.add(trip)
        session.commit()

        yield trip

        session.delete(trip)
        session.commit()


@pytest.fixture
def trip_wizzair_both_ways() -> Trip:
    with Session() as session:
        trip = Trip(
            start_date=pendulum.naive(2024, 4, 13, 4, 0, 0, 0),
            end_date=pendulum.naive(2024, 4, 14, 12, 0, 0, 0),
            currency='CZK',
            outbound_cost=Decimal(120),
            outbound_airport='PRG',
            outbound_airline='Wizz air',
            outbound_fly_number='TEST321',
            return_cost=Decimal(100),
            return_airport='MXP',
            return_airline='Wizz air',
            return_fly_number='TEST123',
        )
        session.add(trip)
        session.commit()

        yield trip

        session.delete(trip)
        session.commit()


@pytest.fixture
def trip_volotea_both_ways() -> Trip:
    with Session() as session:
        trip = Trip(
            start_date=pendulum.naive(2024, 4, 13, 4, 0, 0, 0),
            end_date=pendulum.naive(2024, 4, 14, 12, 0, 0, 0),
            currency='CZK',
            outbound_cost=Decimal(120),
            outbound_airport='PRG',
            outbound_airline='Volotea',
            outbound_fly_number='TEST321',
            return_cost=Decimal(100),
            return_airport='MXP',
            return_airline='Volotea',
            return_fly_number='TEST123',
        )
        session.add(trip)
        session.commit()

        yield trip

        session.delete(trip)
        session.commit()
