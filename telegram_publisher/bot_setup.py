"""Telegram bot setup here."""
from aiogram import Bot

from telegram_publisher.settings import app_settings

bot = Bot(
    token=app_settings.BOT_TOKEN,
    parse_mode='MarkdownV2',
)
