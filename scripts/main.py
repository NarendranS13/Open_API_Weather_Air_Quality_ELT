from .elt_jobs.weather_api import weather_api,air_pollution_data
from .elt_jobs.load_to_s3 import load_to_s3
from .elt_jobs.constants import CITY_LIST
from .config import LOG_DIR, DATA_DIR
import os
from datetime import datetime
import json
from zoneinfo import ZoneInfo
import logging

### setting up an log file path
### Create app.log with timestamp
current_timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

### Create the log filename
log_filename = f"app_{current_timestamp}.log"
log_filepath = os.path.join(LOG_DIR, log_filename)

if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

### Configure the basic logging
logging.basicConfig(
    filename = log_filepath,
    level = logging.INFO,
    format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Create a logger instance for main.py
logger = logging.getLogger(__name__)

### Create the Data Dir to save extracted Data.
os.makedirs(DATA_DIR, exist_ok = True)


logger.info("Data Directory created/present")

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

    weather_path = os.path.join(DATA_DIR, f"weather_data_{today}.json")
    air_quality_path = os.path.join(DATA_DIR, f"air_quality_data_{today}.json")

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