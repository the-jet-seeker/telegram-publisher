from aiogram import types

from telegram_publisher.publisher import _choose_picture


def test_choose_picture_happy_path():
    res = _choose_picture('BUD')

    assert isinstance(res, types.FSInputFile)
    assert 'BUD' in res.filename


def test_choose_picture_default_pic():
    res = _choose_picture('ZZZ')

    assert isinstance(res, types.FSInputFile)
    assert 'default' in res.filename
