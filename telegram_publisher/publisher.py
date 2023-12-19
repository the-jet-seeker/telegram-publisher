"""Fetch trips and publish them to telegram channel."""

import asyncio
import logging

import airportsdata
import pendulum
from aiogram.utils import markdown

from telegram_publisher.bot_setup import bot
from telegram_publisher.schemas import PublisherResponse, Trips, TripsGroup
from telegram_publisher.settings import app_settings
from telegram_publisher.trips_selector import get_top_trips

logger = logging.getLogger(__file__)

airports = airportsdata.load('IATA')


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
            total_cost = trip.outbound_cost + trip.return_cost
            messages.append(markdown.markdown_decoration.quote('{0} {1}'.format(
                total_cost,
                trip.currency,
            )))
            messages.append(markdown.markdown_decoration.quote(
                pendulum.instance(trip.start_date).to_day_datetime_string(),
            ))
            messages.append(markdown.markdown_decoration.quote(
                pendulum.instance(trip.end_date).to_day_datetime_string(),
            ))
            messages.append('')
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
