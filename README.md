# 🧠 Author
Narendran S


[LinkedIN](https://www.linkedin.com/in/narendrans1999/) | [Github](https://github.com/NarendranS13)

# OpenWeather API ELT Project
Developed and ELT project using the OpenWeather API to extract data for weather and air pollution for the 10 Indian Cities.

## Features
Uses Python Requests & Boto3 for AWS Service Automation.
Utilized Airflow for scheduling and orchestration.
.env based configuration (No requirement for AWS CLI)
Implemented Agnostic Folder creation output for storing Data temporarily.

## Steps required to Run the project
1. Creation of the .env file to save OpenWeather API and AWS Access Key, Secret Access Key and default Region.
2. Do not use AWS PROFILE in the .env. This will make boto3 to check for AWS CLI based credentials and config files.
3. For running Airflow in Local Environment. We required Windows Subsytem for Linux (WSL). I used Debian.
4. For .env aws parameters, use the same parameters as recommended in the AWS boto3 docs.

## Activating the environment in windows & Linux
``` terminal
git clone https://github.com/NarendranS13/Open_API_Weather_Air_Quality_ELT
cd Open_API_Weather_Air_Quality_ELT
```

``` terminal
python -m venv _virtual_env_name_
_virtual_env_name_/Scripts/activate
pip install -r requirements.txt
```

``` .env
OPENWEATHER_API_KEY = open_weather_api_key
AWS_ACCESS_KEY_ID = aws_access_key
AWS_SECRET_ACCESS_KEY = aws_secret_access_key
AWS_DEFAULT_REGION = aws_region
S3_BUCKET = s3_bucket
S3_FOLDER = s3_folder
```

## To run the Script on Local Terminal (Windows)

``` terminal
Python main.py
```
## Setting up Airlfow on the Local WSL Linux (Debian)

```bash
sudo apt install python3 python3-venv python3-pip -y
python -m venv airflow_venv
source airflow_venv/bin/activate
AIRFLOW_VERSION=2.9.3
PYTHON_VERSION="$(python --version | cut -d ' ' -f 2 | cut -d '.' -f 1,2)"
CONSTRAINT_URL="https://raw.githubusercontent.com/apache/airflow/constraints-${AIRFLOW_VERSION}/constraints-${PYTHON_VERSION}.txt"
pip install "apache-airflow==${AIRFLOW_VERSION}" --constraint "${CONSTRAINT_URL}"
```

Note: The Above Airflow will utilize the sqlite DB which is only useful for local testing. 

## Setting up the Airlfow (Within the virtual env)
```bash
export AIRFLOW_HOME=~/airflow
airflow db init
airflow users create --username admin --firstname Admin --lastname User --role Admin --email
admin@example.com --password admin
```

## Running the Airflow
``` bash
airlfow scheduler
airflow webserver --port 8080
```

Note: Always start the scheduler and then webserver.


## Airflow Screenshot on local Debian WSL
<img width="1903" height="917" alt="image" src="https://github.com/user-attachments/assets/06abbacb-de9a-4315-9f72-7218ef3f11ab" />

## S3 Upload Successful
<img width="1877" height="796" alt="image" src="https://github.com/user-attachments/assets/58dd06b1-f06e-4596-9c6f-9e629281ebcb" />

