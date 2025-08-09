import os
import tempfile
import json
import pytest
from unittest.mock import patch, MagicMock
from etl.load_to_s3 import load_to_s3

@pytest.fixture
def create_test_files(tmp_path):
    # Create sample weather and air quality files
    weather_file = tmp_path / "weather_data_20250809_120000.json"
    air_quality_file = tmp_path / "air_quality_data_20250809_120000.json"
    
    with open(weather_file, "w") as wf:
        json.dump([{"city_name": "Chennai", "temp": 30}], wf)
    with open(air_quality_file, "w") as af:
        json.dump([{"city_name": "Chennai", "pm2_5": 50}], af)
    
    return tmp_path

@patch("boto3.Session")
def test_s3_upload_success(mock_boto, create_test_files, monkeypatch):
    # Mock environment variables
    monkeypatch.setenv("AWS_ACCESS_KEY_ID", "fake")
    monkeypatch.setenv("AWS_SECRET_ACCESS_KEY", "fake")
    monkeypatch.setenv("AWS_DEFAULT_REGION", "us-east-1")
    monkeypatch.setenv("S3_BUCKET", "test-bucket")
    monkeypatch.setenv("S3_WEATHER_FOLDER", "data/weather")
    monkeypatch.setenv("S3_AIR_QUALITY_FOLDER", "data/air_quality")

    # Mock boto3 upload_file
    mock_client = MagicMock()
    mock_boto.return_value.client.return_value = mock_client

    # Point OUTPUT_DIR to our temp directory
    monkeypatch.setattr("etl.load_to_s3.OUTPUT_DIR", str(create_test_files))

    load_to_s3()

    # Verify upload_file was called twice
    assert mock_client.upload_file.call_count == 2
    args_weather = mock_client.upload_file.call_args_list[0][1]  # kwargs
    args_air = mock_client.upload_file.call_args_list[1][1]

    assert args_weather["Bucket"] == "test-bucket"
    assert args_air["Bucket"] == "test-bucket"
    assert args_weather["Key"].startswith("data/weather")
    assert args_air["Key"].startswith("data/air_quality")
