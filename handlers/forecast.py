from handlers.temperature import get_api_response, get_latitude_longitude
from helper_func import print_error
from Models.forecast_models import (
    GetForecastModel,
    GetForecastReq,
    GetForecastResp,
)
from Models.temperature_models import GetAPIReq, GetLatitudeLongitudeReq
from typing import List

FORECAST_API_URL = "https://api.open-meteo.com/v1/forecast"


def forecast_handler(location: str):
    """Handler for forecast command"""
    try:
        request = GetLatitudeLongitudeReq(location=location)
        response = get_latitude_longitude(request)

        request = GetForecastReq(
            latitude=response.latitude, longitude=response.longitude
        )
        response = get_forecast(request)
        parsed_response = parse_forecast_response(response)
        print(parsed_response)
        return parsed_response
    except Exception as e:
        print_error(e, "Failed to get forecast")


def get_forecast(request: GetForecastReq) -> GetForecastResp:
    """Get Forecast given lat and long"""

    payload = GetForecastModel(
        latitude=request.latitude,
        longitude=request.longitude,
        daily="temperature_2m_max,temperature_2m_min",
        forecast_days=7,
        temperature_unit="fahrenheit",
    )

    api_request = GetAPIReq(api_url=FORECAST_API_URL, params=payload.model_dump())

    response = get_api_response(api_request)
    response_json = response.json()

    response = GetForecastResp(
        latitude=response_json["latitude"],
        longitude=response_json["longitude"],
        temperature_2m_min=response_json["daily"]["temperature_2m_min"],
        temperature_2m_max=response_json["daily"]["temperature_2m_max"],
    )
    return response


def parse_forecast_response(forecast_response: GetForecastResp) -> List:
    min_max_temperatures = []
    for min, max in zip(
        forecast_response.temperature_2m_min, forecast_response.temperature_2m_max
    ):
        min_max_temperatures.append((str(min) + "F - " + str(max) + "F"))
    return min_max_temperatures
