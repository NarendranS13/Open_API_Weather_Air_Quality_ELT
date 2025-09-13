import requests
import os
from dotenv import load_dotenv
import logging


## Get the instance of this module logger

logger = logging.getLogger(__name__)

if os.path.exists("/opt/airflow/project-env/.env"):
    load_dotenv(dotenv_path = "/opt/airflow/project-env/.env")

else:
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

        coord = data.get("coord", {})
        main = data.get("main", {})
        sys = data.get("sys", {})
        wind = data.get("wind", {})

        city_weather = {
            "city_name": city,
            "lat": coord.get("lat"),
            "lon": coord.get("lon"),
            "time_captured": data.get("dt"),
            "temp": main.get("temp"),
            "feels_like": main.get("feels_like"),
            "temp_min": main.get("temp_min"),
            "temp_max": main.get("temp_max"),
            "pressure": main.get("pressure"),
            "humidity": main.get("humidity"),
            "sea_level": main.get("sea_level"),    # optional
            "grnd_level": main.get("grnd_level"),  # optional
            "sunrise": sys.get("sunrise"),
            "sunset": sys.get("sunset"),
            "wind_speed": wind.get("speed"),
            "wind_degree": wind.get("deg"),
            "wind_gust": wind.get("gust"),  # may be None if missing
        }
        logger.info("City level weather data extracted")

        return city_weather
    
    else:
        print("Error", response.status_code, response.text)
        logger.critical(f"Response not found:{response.status_code} and {response.text}")
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
        records = data.get("list") or []
        if not records:
            city_air_quality_data = {
                "city": city,
                "aqi": None,
                "carbon_monoxide": None,
                "nitrogen_monoxide": None,
                "nitrogen_dioxide": None,
                "ozone": None,
                "sulphur_dioxide": None,
                "ammonia": None,
                "pm2_5": None,
                "pm10": None
            }
        else:
            record = records[0] or {}
            main = record.get("main", {})
            comps = record.get("components", {})

            city_air_quality_data = {
                "city": city,
                "aqi": main.get("aqi"),
                "carbon_monoxide": comps.get("co"),
                "nitrogen_monoxide": comps.get("no"),
                "nitrogen_dioxide": comps.get("no2"),
                "ozone": comps.get("o3"),
                "sulphur_dioxide": comps.get("so2"),
                "ammonia": comps.get("nh3"),
                "pm2_5": comps.get("pm2_5"),
                "pm10": comps.get("pm10")
            }
            logger.info("Air quality data available")

            return city_air_quality_data
    
    else:
        print("Error", response.status_code, response.text)
        logger.critical(f"Response not available: {response.status_code} and {response.text}")
        return None
    

