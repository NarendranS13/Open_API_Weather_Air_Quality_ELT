import os
import boto3
from botocore.exceptions import ClientError
from dotenv import load_dotenv
import glob


def load_to_s3():

    load_dotenv()

    ### Create an relative reference to output dir
    output_dir = os.path.join(os.path.dirname(__file__),"..","output")

    ## Import all AWS Information to create boto session for S3 Upload.
    AWS_PROFILE = os.getenv("AWS_PROFILE")
    S3_BUCKET = os.getenv("S3_BUCKET")
    S3_WEATHER_FOLDER = os.getenv("S3_WEATHER_FOLDER")
    S3_AIR_QUALITY_FOLDER = os.getenv("S3_AIR_QUALITY_FOLDER")

    ### Find the latest file in the Output Directory
    weather_files = sorted(glob.glob(os.path.join(output_dir,"weather_data_*.json")), reverse = True)
    air_quality_files = sorted(glob.glob(os.path.join(output_dir,"air_quality_data_*.json")), reverse = True)

    if not weather_files or not air_quality_files:
        print("❌ No Output files found to Upload.")
        return 

    weather_data_file = weather_files[0]
    air_quality_data_file = air_quality_files[0]

    try:
        
        session = boto3.Session(profile_name = AWS_PROFILE)
        s3 = session.client("s3")

        ### Upload the Weather data
        weather_s3_key = f"{S3_WEATHER_FOLDER}/{os.path.basename(weather_data_file)}"
        s3.upload_file(Filename = weather_data_file , Bucket = S3_BUCKET , Key = weather_s3_key )

        ### Upload the air quality data
        air_s3_key = f"{S3_AIR_QUALITY_FOLDER}/{os.path.basename(air_quality_data_file)}"
        s3.upload_file(Filename = air_quality_data_file , Bucket = S3_BUCKET , Key = air_s3_key )

        print("✅ Upload Successfull")

    except ClientError as error:
        print("❌ Upload Failed: {error}")

    return None

# load_to_s3()
    

