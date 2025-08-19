import requests
import os
from dotenv import load_dotenv
import logging


## Get the instance of this module logger

logger = logging.getLogger(__name__)

load_dotenv()

def get_coordinates(city):
    print(f"Getting coordinates for: {city}")
    API_KEY = os.getenv("API_KEY")


    url = "http://api.openweathermap.org/geo/1.0/direct"

    params = {
        "q" : city,
        "appid" : API_KEY,
        "limit" : 2
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        logger.info(f"API is accessable")
        data = response.json()
        if data:
            lat = data[0]["lat"]
            lon = data[0]["lon"]
            # print(f"Coordinates: lat={lat}, lon={lon}")
            return lat, lon

        else:
            logger.info("API not accessable")
            print("No data found for city")

    return None, None


def weather_api(city):


    API_KEY = os.getenv("API_KEY")
    lat,lon = get_coordinates(city)

    url = "https://api.openweathermap.org/data/2.5/weather?"

    params = {
        "lat": lat,
        "lon": lon,
        "appid" : API_KEY,
        "units": "metric",
        "lang": "en"
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()

        city_weather = {
            "city_name": city,
            "lat": data['coord']['lat'],
            "lon": data['coord']['lon'],
            "time_captured": data['dt'],
            "temp": data['main']['temp'],
            "feels_like": data['main']['feels_like'],
            "temp_min": data['main']['temp_min'],
            "temp_max": data['main']['temp_max'],
            "pressure": data['main']['pressure'],
            "humidity": data['main']['humidity'],
            "sea_level": data['main'].get('sea_level'),
            "grnd_level": data['main'].get('grnd_level'),
            "sunrise": data['sys']['sunrise'],
            "sunset": data['sys']['sunset'],
            "wind_speed": data['wind']['speed'],
            "wind_degree": data['wind']['deg'],
            "wind_gust": data['wind']['gust'],

        }
        logger.info("City level weather data extracted")

        return city_weather
    
    else:
        print("Error", response.status_code, response.text)
        logger.CRITICAL(f"Response not found:{response.status_code} and {response.text}")
        return None

def air_pollution_data(city):

    API_KEY = os.getenv("API_KEY")
    lat,lon = get_coordinates(city)

    url = "http://api.openweathermap.org/data/2.5/air_pollution?"

    params = {
        "lat" : lat,
        "lon" : lon,
        "appid" : API_KEY
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        city_air_quality_data = {
            "city": city,
            "aqi": data['list'][0]['main']['aqi'],
            "carbon_monoxide": data['list'][0]['components']['co'],
            "nitrogen_monoxide": data['list'][0]['components']['no'],
            "nitrogen_dioxide": data['list'][0]['components']['no2'],
            "ozone": data['list'][0]['components']['o3'],
            "sulphur_dioxide": data['list'][0]['components']['so2'],
            "ammonia": data['list'][0]['components']['nh3'],
            "pm2_5": data['list'][0]['components']['pm2_5'],
            "pm10": data['list'][0]['components']['pm10']
        }
        logger.info("Air quality data available")

        return city_air_quality_data
    
    else:
        print("Error", response.status_code, response.text)
        logger.CRITICAL(f"Response not available: {response.status_code} and {response.text}")
        return None
    

