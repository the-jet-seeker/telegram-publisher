"""Fetch trips and publish them to telegram channel."""

import asyncio
import logging

import airportsdata
import pendulum
from aiogram import types
from aiogram.utils import markdown

from telegram_publisher.bot_setup import bot
from telegram_publisher.schemas import PublisherResponse, Trips, TripsGroup
from telegram_publisher.settings import app_settings
from telegram_publisher.trips_selector import get_top_trips, get_weekend_range_in_local_tz

logger = logging.getLogger(__file__)

airports = airportsdata.load('IATA')


async def main() -> PublisherResponse:
    """Fetch trips and publish them to telegram channel."""
    weekend_range = get_weekend_range_in_local_tz()

    trips: Trips = get_top_trips(app_settings.TOP_N_TRIPS, weekend_range)
    logger.info('fetch {0} trips'.format(trips))

    if not trips.groups:
        return PublisherResponse(
            is_success=False,
            trips_published=0,
            date_range=weekend_range,
        )

    counter = await _publish(trips.groups)
    logger.info('{0} trips published'.format(counter))

    return PublisherResponse(
        is_success=True,
        trips_published=counter,
        date_range=weekend_range,
    )


async def _publish(trips: list[TripsGroup], welcome_message: str = '') -> int:
    counter: int = 0
    messages = [
        markdown.markdown_decoration.quote(welcome_message),
        markdown.markdown_decoration.quote('Here are your trip ideas for next weekend! 😎 ✈ ✨'),
        '',
    ]

    for trips_group in trips:
        destination: str = airports.get(
            trips_group.destination_code,
            {},
        ).get(
            'city',
            trips_group.destination_code,
        )
        messages.append(markdown.bold('{0} ({1})'.format(
            destination,
            trips_group.destination_code,
        )))

        for trip in trips_group.trips:
            total_cost = round(trip.outbound_cost + trip.return_cost)
            messages.append(markdown.markdown_decoration.quote('{0} {1}'.format(
                total_cost,
                trip.currency.upper(),
            )))
            messages.append(markdown.markdown_decoration.quote('➡ {0}\n{1}'.format(
                pendulum.instance(trip.start_date).format('ddd, MMM D, HH:mm A'),
                trip.outbound_airline,
            )))
            messages.append(markdown.markdown_decoration.quote('⬅ {0}\n{1}'.format(
                pendulum.instance(trip.end_date).format('ddd, MMM D, HH:mm A'),
                trip.return_airline,
            )))
            messages.append('')
            counter += 1

    messages.append(markdown.markdown_decoration.quote(
        """🌈 Have a great weekend! ☀ 💃

If there's anything wrong here, drop me a line and I'll fix it! 😉""",
    ))

    message = markdown.text(*messages, sep='\n')
    logger.info(f'publish message "{message}"')

    await bot.send_photo(
        chat_id=app_settings.PUBLISH_CHANNEL_ID,
        photo=_choose_picture(),
        caption=message,
    )
    return counter


def _choose_picture() -> types.FSInputFile:
    """Choose picture for the post according to the cheapest flight."""
    return types.FSInputFile(f'{app_settings.ASSETS_PATH}/default_1.png')


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(levelname)-8s %(message)s',  # noqa: WPS323
    )

    task_response = asyncio.run(main())
    logger.info('task ended {0}'.format(task_response))
