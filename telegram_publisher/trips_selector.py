"""Trips selectors module."""
import itertools
import logging
import operator
from decimal import Decimal

import pendulum
from pony.orm import db_session

from telegram_publisher.models import Trip
from telegram_publisher.schemas import Trips, TripsGroup
from telegram_publisher.settings import app_settings

logger = logging.getLogger(__file__)


def get_weekend_range_in_local_tz() -> tuple[pendulum.DateTime, pendulum.DateTime]:
    """Return next weekend dates range."""
    today = pendulum.today(app_settings.LOCAL_TIMEZONE)
    weekend_start_date = today.next(day_of_week=pendulum.FRIDAY).set(
        hour=app_settings.MINIMAL_OUTBOUND_FLY_HOUR,
    )
    weekend_end_date = weekend_start_date.next(day_of_week=pendulum.MONDAY).set(
        hour=app_settings.MAXIMUM_RETURN_FLY_HOUR,
    )
    return weekend_start_date, weekend_end_date


def get_top_trips(top_n: int) -> Trips:
    """Return TOP trips by cost grouped by destination."""
    weekend_range = get_weekend_range_in_local_tz()

    trips = _fetch_trips(app_settings.LOCAL_AIRPORT_CODE, *weekend_range)
    logger.info('fetch {0} trips from db for {1} weekend'.format(len(trips), weekend_range))

    # sort by total cost and limiting
    top_by_cost = sorted(
        trips,
        key=lambda trip: trip['outbound_cost'] + trip['return_cost'],
    )[:top_n]
    logger.info('top trips by cost {0}'.format(len(top_by_cost)))

    return Trips(
        groups=_group_by_destination(top_by_cost),
    )


def _group_by_destination(top_by_cost: list[Trip]) -> list[TripsGroup]:
    key_function = operator.itemgetter('return_airport')
    sorted_by_destination = sorted(top_by_cost, key=key_function)

    unsorted_groups: list[tuple[Decimal, TripsGroup]] = []
    for destination_code, group in itertools.groupby(sorted_by_destination, key=key_function):
        group_trips = sorted(
            group,
            key=lambda trip: trip['outbound_cost'] + trip['return_cost'],
        )
        unsorted_groups.append(
            (
                group_trips[0]['outbound_cost'] + group_trips[0]['return_cost'],
                TripsGroup(
                    destination_code=destination_code,
                    trips=group_trips,
                ),
            ),
        )

    return [
        group_trips
        for _, group_trips in sorted(unsorted_groups, key=lambda group_data: group_data[0])
    ]


@db_session
def _fetch_trips(
    outbound_airport_code: str,
    datetime_from: pendulum.DateTime,
    datetime_to: pendulum.DateTime,
) -> list[Trip]:
    # todo impl
    # todo test
    return []
