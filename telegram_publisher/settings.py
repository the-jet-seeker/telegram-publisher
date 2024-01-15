"""Application settings."""
import os
from decimal import getcontext

import pendulum
from pydantic import Field
from pydantic_settings import BaseSettings

getcontext().prec = 2

APP_PATH = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        '..',
    ),
)


class AppSettings(BaseSettings, extra='ignore'):
    """Application settings class."""

    ASSETS_PATH: str = os.path.abspath(
        os.path.join(APP_PATH, 'assets'),
    )

    DEBUG: bool = Field(default=False)
    BOT_TOKEN: str
    PUBLISH_CHANNEL_ID: int = Field(default=-1002080937610)

    DATABASE_USER: str = Field(default='root')
    DATABASE_PASSWORD: str = Field(default='root')
    DATABASE_NAME: str = Field(default='the-jet-seeker')
    DATABASE_HOST: str = Field(default='localhost')
    DATABASE_PORT: int = Field(default=5432)

    TOP_N_TRIPS: int = Field(default=10)
    MINIMAL_OUTBOUND_FLY_HOUR: int = Field(default=19)
    MAXIMUM_RETURN_FLY_HOUR: int = Field(default=11)
    LOCAL_TIMEZONE: pendulum.Timezone = Field(default=pendulum.Timezone('Europe/Prague'))
    LOCAL_AIRPORT_CODE: str = Field(default='PRG')


app_settings = AppSettings(
    _env_file=os.path.join(APP_PATH, '.env'),  # type:ignore
)
