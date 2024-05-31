import pytest

from telegram_publisher.message_presenter import _transform_currency_code


def test_transform_currency_code_happy_path():
    currency = 'czk'

    res = _transform_currency_code(currency)

    assert res == 'Kč'


def test_transform_currency_code_wrong_currency():
    currency = 'test'

    with pytest.raises(RuntimeError):
        _transform_currency_code(currency)

