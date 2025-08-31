FROM python:3.11-slim

WORKDIR /app

ADD requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY scripts/ ./scripts/

RUN mkdir -p /app/logs /app/Data

ENV S3_BUCKET="openweather-api-bucket-dev" \
    S3_WEATHER_FOLDER="data/weather_data" \
    S3_AIR_QUALITY_FOLDER="data/air_quality_data"

CMD ["python","-m","scripts.main"]