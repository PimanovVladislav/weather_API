import os
import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

OPENWEATHER_API_KEY = os.getenv('OPENWEATHER_API_KEY')
BASE_URL = "https://api.openweathermap.org/data/2.5"

def kelvin_to_celsius(kelvin):
    return round(kelvin - 273.15, 1)

def get_current_weather(city):
    url = f"{BASE_URL}/weather"
    params = {
        "q": city,
        "appid": OPENWEATHER_API_KEY,
    }
    resp = requests.get(url, params=params, timeout=5)
    if resp.status_code == 404:
        return None, "City not found"
    if resp.status_code != 200:
        return None, f"External API error: {resp.status_code}"
    data = resp.json()
    temp_c = kelvin_to_celsius(data['main']['temp'])
    tz_offset = data.get('timezone', 0)
    local_time = (datetime.utcnow() + timedelta(seconds=tz_offset)).strftime("%H:%M")
    return {"temperature": temp_c, "local_time": local_time}, None

def get_forecast(city, target_date):
    url = f"{BASE_URL}/forecast"
    params = {
        "q": city,
        "appid": OPENWEATHER_API_KEY,
    }
    resp = requests.get(url, params=params, timeout=5)
    if resp.status_code == 404:
        return None, "City not found"
    if resp.status_code != 200:
        return None, f"External API error: {resp.status_code}"
    data = resp.json()
    temps = []
    for item in data.get('list', []):
        dt_txt = item['dt_txt']
        dt = datetime.strptime(dt_txt, "%Y-%m-%d %H:%M:%S").date()
        if dt == target_date:
            temp_c = kelvin_to_celsius(item['main']['temp'])
            temps.append(temp_c)
    if not temps:
        return None, "No forecast data available for this date"
    return {"min_temperature": min(temps), "max_temperature": max(temps)}, None
