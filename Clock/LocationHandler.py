from geopy.geocoders import Nominatim
from astral import LocationInfo
from astral.sun import sun
from datetime import datetime
from timezonefinder import TimezoneFinder
import pytz

def get_user_location():
    """Prompts user for a city and returns the city name."""
    city = input("Enter your city: ").strip()
    return city

def get_sunrise_sunset(location):
    """
    Fetches latitude and longitude for the given city,
    calculates sunrise and sunset times adjusted for timezone.
    """
    geolocator = Nominatim(user_agent="clock_app")
    location_data = geolocator.geocode(location)
    
    if not location_data:
        raise ValueError(f"City '{location}' not found. Please try again.")

    # Get timezone using TimezoneFinder
    tf = TimezoneFinder()
    timezone_str = tf.timezone_at(lng=location_data.longitude, lat=location_data.latitude)

    if not timezone_str:
        raise ValueError(f"Timezone for city '{location}' could not be determined.")

    # Set up city information with timezone
    city_info = LocationInfo(location_data.address, "Unknown", timezone_str,
                             location_data.latitude, location_data.longitude)

    # Calculate sunrise and sunset times in local time
    s = sun(city_info.observer, date=datetime.now(), tzinfo=pytz.timezone(timezone_str))

    return {
        'sunrise': s['sunrise'].astimezone(pytz.timezone(timezone_str)),
        'sunset': s['sunset'].astimezone(pytz.timezone(timezone_str)),
    }
