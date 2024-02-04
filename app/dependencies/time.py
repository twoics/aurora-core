from datetime import datetime
from datetime import timezone

import pytz
from fastapi import Depends

from app.config.config import Settings
from app.dependencies.config import get_settings


def current_utctime() -> datetime:
    """Get current UTC time"""

    return datetime.now(timezone.utc)


def current_ztime(settings: Settings = Depends(get_settings)) -> datetime:
    """Get current ZONE time, zone selected in .env"""

    local_timezone = pytz.timezone(settings.TIME_ZONE)
    return datetime.now(local_timezone)
