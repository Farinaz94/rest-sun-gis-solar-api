from datetime import datetime
from zoneinfo import ZoneInfo  # or use `pytz` for Python <3.9
import httpx
import logging

logger = logging.getLogger(__name__)

def get_timezone_from_ip(ip: str) -> str:
    """
    Get timezone string from an IP address using the ipwho.is API.
    Falls back to 'UTC' if the timezone cannot be determined.
    """
    try:
        response = httpx.get(f"https://ipwho.is/{ip}", timeout=3.0)
        if response.status_code == 200:
            data = response.json()
            tz = data.get("timezone", {}).get("id")
            if tz:
                return tz
            else:
                logger.warning(f"No timezone found in response for IP {ip}. Response: {data}")
        else:
            logger.warning(f"ipwho.is returned status {response.status_code} for IP {ip}")
    except Exception as e:
        logger.warning(f"Error fetching timezone for IP {ip}: {e}")
    
    return "UTC"

def convert_to_user_time(utc_dt: datetime, timezone_id: str) -> str:
    """
    Convert UTC datetime to user's timezone.
    """
    try:
        return utc_dt.astimezone(ZoneInfo(timezone_id)).strftime('%Y-%m-%d %H:%M:%S')
    except Exception as e:
        logger.warning(f"Could not convert time to {timezone_id}: {e}")
        return utc_dt.strftime('%Y-%m-%d %H:%M:%S')
