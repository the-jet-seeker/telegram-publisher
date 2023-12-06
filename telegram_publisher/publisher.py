"""Fetch trips and publish them to telegram channel."""

import asyncio
import logging
from dataclasses import dataclass

from pony.orm import db_session

from telegram_publisher.bot_setup import bot
from telegram_publisher.models import Trip
from telegram_publisher.settings import app_settings

logger = logging.getLogger(__file__)


@dataclass
class PublisherResult:
    """Task response schema."""

    is_success: bool
    trips_published: int = 0


async def main() -> PublisherResult:
    """Fetch trips and publish them to telegram channel."""
    trips = _get_trips()
    logger.info('fetch {0} trips'.format(len(trips)))

    if trips:
        await _publish(trips)
        logger.info('trips published')

    return PublisherResult(
        is_success=bool(trips),
        trips_published=len(trips),
    )


@db_session
def _get_trips() -> list[Trip]:
    # todo impl
    # todo test
    return []


async def _publish(trips: list[Trip]) -> int:
    # todo test
    messages = [
        'Cheap-trips are here!',
    ]
    for index, trip in enumerate(trips):
        messages.append(f'{index}: {trip.id}')

    message = '\n'.join(messages)
    logger.info(f'publish message "{message}"')

    await bot.send_message(app_settings.PUBLISH_CHANNEL_ID, message)

    return len(trips)


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(levelname)-8s %(message)s',  # noqa: WPS323
    )
    asyncio.run(main())
