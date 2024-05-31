"""Prepare and publish messages about trips to the telegram channel."""
import logging
from urllib.parse import urlencode

import airportsdata
import pendulum
import pycountry
from aiogram.utils import markdown

from telegram_publisher import models, schemas
from telegram_publisher.settings import app_settings

logger = logging.getLogger(__file__)

airports = airportsdata.load('IATA')


def message_presenter(trips: list[schemas.TripsGroup]) -> tuple[str, int]:
    """Create the text for trips post."""
    # todo test
    counter: int = 0
    messages = [
        markdown.markdown_decoration.quote('Here are your trip ideas for next weekend! 😎 🗺 ✈ ✨'),
        '',
    ]

    for trips_group in trips:
        destination = airports.get(
            trips_group.destination_code,
            {},
        )
        destination_country_code: str = destination.get(
            'country',
            trips_group.destination_code,
        )
        destination_country = pycountry.countries.get(alpha_2=destination_country_code)
        messages.append(markdown.bold('{0} {1}'.format(
            destination_country.name,
            destination_country.flag,
        )))
        messages.append(markdown.markdown_decoration.quote('{0} ({1})'.format(
            destination.get(
                'city',
                trips_group.destination_code,
            ),
            trips_group.destination_code,
        )))

        for trip in trips_group.trips:
            messages += _trip_description(trip)

            counter += 1

    messages.append(
        markdown.markdown_decoration.quote('🌈 Have a great weekend! ☀ 💃'),
    )

    return (
        markdown.text(*messages, sep='\n'),
        counter,
    )


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
        '► {0} {1}'.format(
            pendulum.instance(trip.start_date).format('ddd, MMM D, HH:mm'),
            _airline_ticket_url(trip).outbound_ticket_link,
        ),
        '◄ {0} {1}'.format(
            pendulum.instance(trip.end_date).format('ddd, MMM D, HH:mm'),
            _airline_ticket_url(trip).inbound_ticket_link,
        ),
    ]

    if trip.rent_cost:
        trip_description.append(markdown.markdown_decoration.quote('🏠 {0} {1}   ☕️ {2} {3}'.format(
            round(trip.rent_cost * trip.duration_nights),
            currency,
            round(trip.meal_cost * trip.meals_amount),
            currency,
        )))

    trip_description.append('')

    return trip_description


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
