import os
import boto3
from botocore.exceptions import ClientError
from dotenv import load_dotenv
import glob
from ..config import DATA_DIR
import logging

# Get the logger for this instance
logger = logging.getLogger(__name__)

def load_to_s3():

    logger.info("Load to S3 Module started")
    if os.path.exists("/opt/airflow/project-env/.env"):
        load_dotenv(dotenv_path = "/opt/airflow/project-env/.env")
    else:
        load_dotenv()

    # ### Create an relative reference to output dir
    # output_dir = os.path.join(os.path.dirname(__file__),"..","output")

    ## Import all AWS Information to create boto session for S3 Upload.
    S3_BUCKET = os.getenv("S3_BUCKET")
    S3_WEATHER_FOLDER = os.getenv("S3_WEATHER_FOLDER")
    S3_AIR_QUALITY_FOLDER = os.getenv("S3_AIR_QUALITY_FOLDER")
    AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
    AWS_DEFAULT_REGION = os.getenv("AWS_DEFAULT_REGION")

    ### Find the latest file in the Output Directory
    weather_files = sorted(glob.glob(os.path.join(DATA_DIR,"weather_data_*.json")), reverse = True)
    air_quality_files = sorted(glob.glob(os.path.join(DATA_DIR,"air_quality_data_*.json")), reverse = True)

    if not weather_files or not air_quality_files:
        print("❌ No Output files found to Upload.")
        logger.warning("No Output file present")
        return 

    weather_data_file = weather_files[0]
    air_quality_data_file = air_quality_files[0]

    try:
        
        # session = boto3.Session(profile_name = AWS_PROFILE)

        # s3 = session.client("s3",
        # aws_access_key_id = AWS_ACCESS_KEY_ID,
        # aws_secret_access_key = AWS_SECRET_KEY,
        # region_name = AWS_REGION
        # )

        session = boto3.Session(
            aws_access_key_id = AWS_ACCESS_KEY_ID,
            aws_secret_access_key = AWS_SECRET_ACCESS_KEY,
            region_name = AWS_DEFAULT_REGION
        )

        s3 = session.client("s3")

        ### Upload the Weather data
        weather_s3_key = f"{S3_WEATHER_FOLDER}/{os.path.basename(weather_data_file)}"
        s3.upload_file(Filename = weather_data_file , Bucket = S3_BUCKET , Key = weather_s3_key )

        ### Upload the air quality data
        air_s3_key = f"{S3_AIR_QUALITY_FOLDER}/{os.path.basename(air_quality_data_file)}"
        s3.upload_file(Filename = air_quality_data_file , Bucket = S3_BUCKET , Key = air_s3_key )

        print("✅ Upload Successfull")
        logger.info("S3 UPLOAD Succesfull")

    except ClientError as error:
        print("❌ Upload Failed: {error}")
        logger.critical(f"Failed to upload the files to S3: {error}")

    return None

# load_to_s3()
    

