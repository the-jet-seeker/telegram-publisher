from telegram_publisher.models import Trip
from telegram_publisher.publisher import _airline_ticket_url
from telegram_publisher.schemas import AirlineTicketUrl


def test_airline_ticket_url_ryanair_happy_path(trip_ryanair_both_ways: Trip):
    res = _airline_ticket_url(trip_ryanair_both_ways)

    assert isinstance(res, AirlineTicketUrl)
    assert res.outbound_ticket_link == '[Ryanair](https://www.ryanair.com/gb/en/trip/flights/select?adults=1&teens=0&children=0&infants=0&dateOut=2024-03-09&dateIn=&isConnectedFlight=false&discount=0&isReturn=false&promoCode=&originIata=PRG&destinationIata=BLQ&tpAdults=1&tpTeens=0&tpChildren=0&tpInfants=0&tpStartDate=2024-03-09&tpEndDate=&tpDiscount=0&tpPromoCode=&tpOriginIata=PRG&tpDestinationIata=BLQ)'
    assert res.inbound_ticket_link ==  '[Ryanair](https://www.ryanair.com/gb/en/trip/flights/select?adults=1&teens=0&children=0&infants=0&dateOut=2024-03-10&dateIn=&isConnectedFlight=false&discount=0&isReturn=false&promoCode=&originIata=BLQ&destinationIata=PRG&tpAdults=1&tpTeens=0&tpChildren=0&tpInfants=0&tpStartDate=2024-03-10&tpEndDate=&tpDiscount=0&tpPromoCode=&tpOriginIata=BLQ&tpDestinationIata=PRG)'


def test_airline_ticket_url_other_airline(trip_first: Trip):
    res = _airline_ticket_url(trip_first)

    assert res.outbound_ticket_link == 'TEST airlines'
    assert res.inbound_ticket_link == 'TEST airlines'
