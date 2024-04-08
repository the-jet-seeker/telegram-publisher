from telegram_publisher.models import Trip
from telegram_publisher.publisher import _airline_ticket_url
from telegram_publisher.schemas import AirlineTicketUrl


def test_airline_ticket_url_ryanair_happy_path(trip_ryanair_both_ways: Trip):
    res = _airline_ticket_url(trip_ryanair_both_ways)

    assert isinstance(res, AirlineTicketUrl)
    assert res.outbound_ticket_link == '[Ryanair](https://www.ryanair.com/gb/en/trip/flights/select?adults=1&teens=0&children=0&infants=0&dateOut=2024-03-09&dateIn=&isConnectedFlight=false&discount=0&isReturn=false&promoCode=&originIata=PRG&destinationIata=BLQ&tpAdults=1&tpTeens=0&tpChildren=0&tpInfants=0&tpStartDate=2024-03-09&tpEndDate=&tpDiscount=0&tpPromoCode=&tpOriginIata=PRG&tpDestinationIata=BLQ)'
    assert res.inbound_ticket_link ==  '[Ryanair](https://www.ryanair.com/gb/en/trip/flights/select?adults=1&teens=0&children=0&infants=0&dateOut=2024-03-10&dateIn=&isConnectedFlight=false&discount=0&isReturn=false&promoCode=&originIata=BLQ&destinationIata=PRG&tpAdults=1&tpTeens=0&tpChildren=0&tpInfants=0&tpStartDate=2024-03-10&tpEndDate=&tpDiscount=0&tpPromoCode=&tpOriginIata=BLQ&tpDestinationIata=PRG)'


def test_airline_ticket_url_easyjet_happy_path(trip_easyjet_both_ways: Trip):
    res = _airline_ticket_url(trip_easyjet_both_ways)

    assert isinstance(res, AirlineTicketUrl)
    assert res.outbound_ticket_link == '[easyJet](https://worldwide.easyjet.com/search?origins=PRG&destinations=MXP&departureDate=2024-04-12&isOneWay=true&currency=CZK&residency=CZ&utm_source=easyjet_search_pod&adult=16&partner=easyjet)'
    assert res.inbound_ticket_link == '[easyJet](https://worldwide.easyjet.com/search?origins=MXP&destinations=PRG&departureDate=2024-04-14&isOneWay=true&currency=CZK&residency=CZ&utm_source=easyjet_search_pod&adult=16&partner=easyjet)'


def test_airline_ticket_url_wizzair_happy_path(trip_wizzair_both_ways: Trip):
    res = _airline_ticket_url(trip_wizzair_both_ways)

    assert isinstance(res, AirlineTicketUrl)
    assert res.outbound_ticket_link == '[Wizz air](https://wizzair.com/en-gb/booking/select-flight/PRG/MXP/2024-04-13/null/1/0/0/null)'
    assert res.inbound_ticket_link == '[Wizz air](https://wizzair.com/en-gb/booking/select-flight/MXP/PRG/2024-04-14/null/1/0/0/null)'


def test_airline_ticket_url_volotea_happy_path(trip_volotea_both_ways: Trip):
    res = _airline_ticket_url(trip_volotea_both_ways)

    assert isinstance(res, AirlineTicketUrl)
    assert res.outbound_ticket_link == '[Volotea](https://www.volotea.com/en/direct-flights/)'
    assert res.inbound_ticket_link == '[Volotea](https://www.volotea.com/en/direct-flights/)'


def test_airline_ticket_url_other_airline(trip_first: Trip):
    res = _airline_ticket_url(trip_first)

    assert res.outbound_ticket_link == 'TEST airlines'
    assert res.inbound_ticket_link == 'TEST airlines'
