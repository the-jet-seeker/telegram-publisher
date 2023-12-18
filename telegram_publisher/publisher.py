"""Fetch trips and publish them to telegram channel."""

import asyncio
import logging

import pendulum
from aiogram.utils import markdown
from pony.orm import db_session

from telegram_publisher.bot_setup import bot
from telegram_publisher.models import Trip
from telegram_publisher.schemas import PublisherResponse, TripsGroup, Trips
from telegram_publisher.settings import app_settings

logger = logging.getLogger(__file__)


async def main() -> PublisherResponse:
    """Fetch trips and publish them to telegram channel."""
    trips: Trips = _get_top_trips()
    logger.info('fetch {0} trips'.format(trips))

    if not trips.groups:
        return PublisherResponse(
            is_success=False,
            trips_published=0,
        )

    counter = await _publish(trips.groups)
    logger.info('%d trips published'.format(counter))
    return PublisherResponse(
        is_success=True,
        trips_published=counter,
    )


def _get_top_trips() -> Trips:
    # todo test
    today_utc = pendulum.now(pendulum.UTC)
    weekend_start_date_utc = today_utc.next(day_of_week=pendulum.FRIDAY)

    trips = _fetch_trips(weekend_start_date_utc)
    logger.info('fetch %d trips from db for %s weekend'.format(len(trips), weekend_start_date_utc))

    # todo impl

    return Trips(
        groups=[],
        weekend_start_date_utc=weekend_start_date_utc,
    )


@db_session
def _fetch_trips(date_from_utc: pendulum.datetime) -> list[Trip]:
    # todo impl
    # todo test
    return []


async def _publish(trips: list[TripsGroup], welcome_message: str = '') -> int:
    counter: int = 0
    messages = [
        welcome_message,
        'Cheap\-trips are here\!',
        '',
    ]

    for trips_group in trips:
        messages.append(markdown.bold(trips_group.destination_code))
        for index, trip in enumerate(trips_group.trips):
            messages.append(f'Trip id\#{trip.id}')
            counter += 1

    message = markdown.text(*messages, sep='\n')
    logger.info(f'publish message "{message}"')

    await bot.send_message(app_settings.PUBLISH_CHANNEL_ID, message)
    return counter


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(levelname)-8s %(message)s',  # noqa: WPS323
    )
    asyncio.run(main())
