"""Telegram bot setup here."""
from aiogram import Bot
from aiogram.client.session.aiohttp import AiohttpSession

from telegram_publisher.settings import app_settings

session = AiohttpSession()
bot = Bot(
    token=app_settings.BOT_TOKEN,
    parse_mode='MarkdownV2',
    session=session,
)
