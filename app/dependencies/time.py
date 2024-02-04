from datetime import datetime
from datetime import timezone
from typing import Annotated

import pytz
from fastapi import Depends

from app.dependencies.config import get_settings


def current_utctime() -> datetime:
    """Get current UTC time"""

    return datetime.now(timezone.utc)


def current_ztime(settings: Annotated[get_settings, Depends()]) -> datetime:
    """Get current ZONE time, zone selected in .env"""

    local_timezone = pytz.timezone(settings.TIME_ZONE)
    return datetime.now(local_timezone)
