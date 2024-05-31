"""Fetch trips and publish them to telegram channel."""

import asyncio
import logging
import os
import random

from aiogram import types

from telegram_publisher import bot_setup, schemas
from telegram_publisher.message_presenter import message_presenter
from telegram_publisher.settings import app_settings
from telegram_publisher.trips_selector import get_top_trips, get_weekend_range_in_local_tz

logger = logging.getLogger(__file__)


async def main() -> schemas.PublisherResponse:
    """Fetch trips and publish them to telegram channel."""
    weekend_range = get_weekend_range_in_local_tz()

    trips: schemas.Trips = get_top_trips(app_settings.TOP_N_TRIPS, weekend_range)
    logger.info('fetch {0} trips'.format(trips))

    counter = 0
    is_success = False
    if trips.groups:
        counter = await _publish(trips.groups)
        is_success = True
        logger.info('{0} trips published'.format(counter))

    await bot_setup.session.close()

    return schemas.PublisherResponse(
        is_success=is_success,
        trips_published=counter,
        date_range=weekend_range,
    )


async def _publish(trips: list[schemas.TripsGroup]) -> int:
    """Publish a messages to the channel. Return amount of trips."""
    message, counter = message_presenter(trips)

    logger.info(f'publish message "{message}"')

    await bot_setup.bot.send_photo(
        chat_id=app_settings.PUBLISH_CHANNEL_ID,
        photo=_choose_picture(trips[0].destination_code.upper()),
        caption=message,
    )
    return counter


def _choose_picture(dst_airport: str) -> types.FSInputFile:
    """Choose picture for the post according to the cheapest flight."""
    all_pics = [
        pic
        for pic in os.listdir(app_settings.ASSETS_PATH)
        if os.path.isfile(os.path.join(app_settings.ASSETS_PATH, pic))
    ]

    arr_airport_pics = [
        pic
        for pic in all_pics
        if pic.startswith(dst_airport)
    ]
    default_pic = [
        pic
        for pic in all_pics
        if pic.startswith('default')
    ]

    pic_name = random.choice(arr_airport_pics or default_pic)

    return types.FSInputFile(
        str(os.path.join(app_settings.ASSETS_PATH, pic_name)),
    )


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(levelname)-8s %(message)s',  # noqa: WPS323
    )

    task_response = asyncio.run(main())
    logger.info('task ended {0}'.format(task_response))
