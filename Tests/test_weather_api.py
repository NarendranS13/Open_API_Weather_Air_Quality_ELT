import pytest
from ..scripts.elt_jobs import weather_api as weather_api_module
from ..scripts.elt_jobs.weather_api import weather_api, air_pollution_data


def test_weather_api_valid_city(monkeypatch):
    def mock_response(city):
        return{'city_name': city, 'temp': 30, 'humidity': 77}

    monkeypatch.setattr(weather_api_module,'weather_api', mock_response)
    result = weather_api('Chennai')
    assert result['city_name'] == 'Chennai'
    assert 'temp' in result
    assert 'humidity' in result


def test_air_quality_valid_city(monkeypatch):
    def mock_response(city):
        return{"city": city, "aqi":3, "ammonia": 567}
    
    monkeypatch.setattr(weather_api_module,"air_pollution_data", mock_response)
    result = air_pollution_data("Kolkata")
    assert result['city'] == "Kolkata"
    assert 'aqi' in result
    assert 'ammonia' in result

