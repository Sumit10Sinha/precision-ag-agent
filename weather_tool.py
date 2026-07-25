from langchain_core.tools import tool
import requests

@tool
def get_weather_forecast(lat: float = 22.42, lon: float = 87.32) -> float:
    """
    Fetches daily precipitation forecast in millimeters using the Open-Meteo API.
    Use this tool when you need to check expected rainfall for a farm location.
    Default coordinates are for Midnapore, West Bengal.
    """
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&daily=precipitation_sum&timezone=auto"
    
    try:
        response = requests.get(url)
        data = response.json()
        todays_rain = data['daily']['precipitation_sum'][0]
        return float(todays_rain)
    except Exception as e:
        print(f"Error fetching weather: {e}")
        return 0.0