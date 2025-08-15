from etl.weather_api import weather_api,air_pollution_data
from etl.load_to_s3 import load_to_s3
from etl.constants import CITY_LIST
from config import OUTPUT_DIR
import os
from datetime import datetime
import json
from zoneinfo import ZoneInfo
import logging

### setting up an log file path
log_directory = "logs"
log_filename = "app.log"
log_filepath = os.path.join(log_directory, log_filename)

if not os.path.exists(log_directory):
    os.makedirs(log_directory)

### Configure the basic logging
logging.basicConfig(
    filename = log_filepath,
    level = logging.INFO,
    format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Create a logger instance for main.py
logger = logging.getLogger(__name__)

### Create the ouptut Dir

os.makedirs(OUTPUT_DIR, exist_ok = True)
logger.info("Output Directory created/present")

def main():
    logger.info("Starting the main data pipeline.")
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
    
    # print("Air Quality Data:",all_city_air_data)
    # print("Weather Data:",all_city_weather_data)

    ## Save the Output in JSON format in Output dir using IST (Indian Standard Time)

    now_ist = datetime.now(ZoneInfo("Asia/Kolkata"))
    today = now_ist.strftime('%Y%m%d_%H%M%S')

    ## Create the file paths in Output DIR

    weather_path = os.path.join(OUTPUT_DIR, f"weather_data_{today}.json")
    air_quality_path = os.path.join(OUTPUT_DIR, f"air_quality_data_{today}.json")

    ## Save the output in JSON
    with open(weather_path, "w") as wf:
        json.dump(all_city_weather_data, wf, indent=4)

    with open(air_quality_path, "w") as af:
        json.dump(all_city_air_data, af, indent=4)

    ### Loading the data into s3
    
    load_to_s3()


    logging.info("Main data pipeline finished successfully")



if __name__ == "__main__":
    main()