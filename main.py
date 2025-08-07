from etl.weather_api import weather_api,air_pollution_data
from etl.constants import CITY_LIST

def main():
    all_city_weather_data = []
    all_city_air_data = []
    for city in CITY_LIST:
        # if city != 'Chennai':
        #     continue
        weather = weather_api(city)
        air = air_pollution_data(city)
        if weather:
            all_city_weather_data.append(weather)
        if air:
            all_city_air_data.append(air)
    
    print("Air Quality Data:",all_city_air_data)
    print("Weather Data:",all_city_weather_data)




if __name__ == "__main__":
    main()