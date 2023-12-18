"""Fetch trips and publish them to telegram channel."""

import asyncio
import logging

from aiogram.utils import markdown

from telegram_publisher.bot_setup import bot
from telegram_publisher.schemas import PublisherResponse, Trips, TripsGroup
from telegram_publisher.settings import app_settings
from telegram_publisher.trips_selector import get_top_trips

logger = logging.getLogger(__file__)


async def main() -> PublisherResponse:
    """Fetch trips and publish them to telegram channel."""
    trips: Trips = get_top_trips(app_settings.TOP_N_TRIPS)
    logger.info('fetch {0} trips'.format(trips))

    if not trips.groups:
        return PublisherResponse(
            is_success=False,
            trips_published=0,
        )

    counter = await _publish(trips.groups)
    logger.info('{0} trips published'.format(counter))

    return PublisherResponse(
        is_success=True,
        trips_published=counter,
    )


async def _publish(trips: list[TripsGroup], welcome_message: str = '') -> int:
    counter: int = 0
    messages = [
        markdown.markdown_decoration.quote(welcome_message),
        markdown.markdown_decoration.quote('Cheap-trips are here!'),
        '',
    ]

    for trips_group in trips:
        messages.append(markdown.bold(trips_group.destination_code))
        for trip in trips_group.trips:
            messages.append(markdown.markdown_decoration.quote(f'Trip id#{trip.id}'))
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
