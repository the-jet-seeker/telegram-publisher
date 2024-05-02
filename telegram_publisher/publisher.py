"""Fetch trips and publish them to telegram channel."""

import asyncio
import logging
import os
import random
from urllib.parse import urlencode

import airportsdata
import pendulum
from aiogram import types
from aiogram.utils import markdown

from telegram_publisher import bot_setup, models, schemas
from telegram_publisher.settings import app_settings
from telegram_publisher.trips_selector import get_top_trips, get_weekend_range_in_local_tz

logger = logging.getLogger(__file__)

airports = airportsdata.load('IATA')


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


async def _publish(trips: list[schemas.TripsGroup], welcome_message: str = '') -> int:
    counter: int = 0
    messages = [
        markdown.markdown_decoration.quote(welcome_message),
        markdown.markdown_decoration.quote('Here are your trip ideas for next weekend! 😎 🗺 ✈ ✨'),
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
            messages += _trip_description(trip)

            counter += 1

    messages.append(
        "{0}\n\nIf there's anything wrong here, {1} {2}".format(
            markdown.markdown_decoration.quote('🌈 Have a great weekend! ☀ 💃'),
            markdown.link('drop me', 'https://t.me/eira_tauraco'),
            markdown.markdown_decoration.quote("a line and I'll fix it! 😉"),
        ),
    )

    message = markdown.text(*messages, sep='\n')
    logger.info(f'publish message "{message}"')

    await bot_setup.bot.send_photo(
        chat_id=app_settings.PUBLISH_CHANNEL_ID,
        photo=_choose_picture(trips[0].destination_code.upper()),
        caption=message,
    )
    return counter


def _transform_currency_code(currency: str) -> str:
    """Get currency code from the trip, Return it in the human-readable view."""
    if currency.lower() == 'czk':
        return 'Kč'

    raise RuntimeError("Let's make currency human-readable.")


def _trip_description(trip: models.Trip) -> list[str]:
    """Return a part of the message with one trip."""
    total_cost = round(trip.outbound_cost + trip.return_cost)
    currency = _transform_currency_code(trip.currency)

    trip_description = [
        markdown.bold('{0} {1}'.format(
            total_cost,
            currency,
        )),
        '🛫 {0} {1}'.format(
            pendulum.instance(trip.start_date).format('ddd, MMM D, HH:mm A'),
            _airline_ticket_url(trip).outbound_ticket_link,
        ),
        '🛬 {0} {1}'.format(
            pendulum.instance(trip.end_date).format('ddd, MMM D, HH:mm A'),
            _airline_ticket_url(trip).inbound_ticket_link,
        ),
    ]

    if trip.rent_cost:
        trip_description.append(markdown.markdown_decoration.quote('approx cost for {0} day(s):'.format(
            trip.duration_nights,
        )))
        trip_description.append(markdown.markdown_decoration.quote('🏠 {0} {1}   ☕️ {2} {3}'.format(
            round(trip.rent_cost * trip.duration_nights),
            currency,
            round(trip.meal_cost * trip.meals_amount),
            currency,
        )))

    trip_description.append('')

    return trip_description


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


def _airline_ticket_url(trip: models.Trip) -> schemas.AirlineTicketUrl:
    """Create a link for the ticket at the airline page."""
    if trip.outbound_airline.lower() == 'ryanair':
        outbound_query_params = urlencode({
            'adults': 1,
            'teens': 0,
            'children': 0,
            'infants': 0,
            'dateOut': trip.start_date.strftime('%Y-%m-%d'),
            'dateIn': '',
            'isConnectedFlight': 'false',
            'discount': 0,
            'isReturn': 'false',
            'promoCode': '',
            'originIata': app_settings.LOCAL_AIRPORT_CODE,
            'destinationIata': trip.return_airport,
            'tpAdults': 1,
            'tpTeens': 0,
            'tpChildren': 0,
            'tpInfants': 0,
            'tpStartDate': trip.start_date.strftime('%Y-%m-%d'),
            'tpEndDate': '',
            'tpDiscount': 0,
            'tpPromoCode': '',
            'tpOriginIata': app_settings.LOCAL_AIRPORT_CODE,
            'tpDestinationIata': trip.return_airport,
        })
        inbound_query_params = urlencode({
            'adults': 1,
            'teens': 0,
            'children': 0,
            'infants': 0,
            'dateOut': trip.end_date.strftime('%Y-%m-%d'),
            'dateIn': '',
            'isConnectedFlight': 'false',
            'discount': 0,
            'isReturn': 'false',
            'promoCode': '',
            'originIata': trip.return_airport,
            'destinationIata': app_settings.LOCAL_AIRPORT_CODE,
            'tpAdults': 1,
            'tpTeens': 0,
            'tpChildren': 0,
            'tpInfants': 0,
            'tpStartDate': trip.end_date.strftime('%Y-%m-%d'),
            'tpEndDate': '',
            'tpDiscount': 0,
            'tpPromoCode': '',
            'tpOriginIata': trip.return_airport,
            'tpDestinationIata': app_settings.LOCAL_AIRPORT_CODE,
        })
        outbound_url = 'https://www.ryanair.com/gb/en/trip/flights/select?{0}'.format(outbound_query_params)
        inbound_url = 'https://www.ryanair.com/gb/en/trip/flights/select?{0}'.format(inbound_query_params)

        return schemas.AirlineTicketUrl(
            outbound_ticket_link=markdown.link(trip.outbound_airline, outbound_url),
            inbound_ticket_link=markdown.link(trip.outbound_airline, inbound_url),
        )

    elif trip.outbound_airline.lower() == 'wizz air':
        outbound_url = 'https://wizzair.com/en-gb/booking/select-flight/{0}/{1}/{2}/null/1/0/0/null'.format(
            app_settings.LOCAL_AIRPORT_CODE,
            trip.return_airport,
            trip.start_date.strftime('%Y-%m-%d'),
        )
        inbound_url = 'https://wizzair.com/en-gb/booking/select-flight/{0}/{1}/{2}/null/1/0/0/null'.format(
            trip.return_airport,
            app_settings.LOCAL_AIRPORT_CODE,
            trip.end_date.strftime('%Y-%m-%d'),
        )
        return schemas.AirlineTicketUrl(
            outbound_ticket_link=markdown.link(trip.outbound_airline, outbound_url),
            inbound_ticket_link=markdown.link(trip.outbound_airline, inbound_url),
        )

    elif trip.outbound_airline.lower() == 'volotea':
        url = 'https://www.volotea.com/en/direct-flights/'
        return schemas.AirlineTicketUrl(
            outbound_ticket_link=markdown.link(trip.outbound_airline, url),
            inbound_ticket_link=markdown.link(trip.outbound_airline, url),
        )

    elif trip.outbound_airline.lower() == 'easyjet':
        outbound_query_params = urlencode({
            'origins': app_settings.LOCAL_AIRPORT_CODE,
            'destinations': f'{trip.return_airport}',
            'departureDate': trip.start_date.strftime('%Y-%m-%d'),
            'isOneWay': 'true',
            'currency': 'CZK',
            'residency': 'CZ',
            'utm_source': 'easyjet_search_pod',
            'adult': 16,
            'partner': 'easyjet',
        })
        inbound_query_params = urlencode({
            'origins': f'{trip.return_airport}',
            'destinations': app_settings.LOCAL_AIRPORT_CODE,
            'departureDate': trip.end_date.strftime('%Y-%m-%d'),  # а не будет ли тут проблемы если прилет заполночь?
            'isOneWay': 'true',
            'currency': 'CZK',
            'residency': 'CZ',
            'utm_source': 'easyjet_search_pod',
            'adult': 16,
            'partner': 'easyjet',
        })

        outbound_url = 'https://worldwide.easyjet.com/search?{0}'.format(outbound_query_params)
        inbound_url = 'https://worldwide.easyjet.com/search?{0}'.format(inbound_query_params)

        return schemas.AirlineTicketUrl(
            outbound_ticket_link=markdown.link(trip.outbound_airline, outbound_url),
            inbound_ticket_link=markdown.link(trip.outbound_airline, inbound_url),
        )

    return schemas.AirlineTicketUrl(
        outbound_ticket_link=trip.outbound_airline,
        inbound_ticket_link=trip.return_airline,
    )


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(levelname)-8s %(message)s',  # noqa: WPS323
    )

    task_response = asyncio.run(main())
    logger.info('task ended {0}'.format(task_response))
