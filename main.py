import argparse
import requests
from typing import List
import json

from Models.base_models import (
    GetTemperatureModel,
    GetLatitudeLongitudeReq,
    GetLatitudeLongitudeResp,
    GetAPIReq,
    GetTemperatureReq,
    GetTemperatureResp,
)

from helper_func import print_error

# add this to a env file
GEOCODING_API_URL = "https://geocoding-api.open-meteo.com/v1/search"
TEMPERATURE_API_URL = "https://api.open-meteo.com/v1/forecast"


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    temperature_parser = subparsers.add_parser(
        "temperature", help="Get today's temperature"
    )
    temperature_parser.add_argument("city", help="name of city")

    args = parser.parse_args()

    commands = {"temperature": lambda: temperature_handler(args.city)}

    command_func = commands.get(args.command)

    if command_func:
        command_func()
    else:
        parser.print_help()


def temperature_handler(location: str):
    """Handler for temperature command"""
    request = GetLatitudeLongitudeReq(location=location)
    try:
        response = get_latitude_longitude(request)
    except Exception as e:
        print_error(e, "Failed to get latitude and longitude")

    request = GetTemperatureReq(
        latitude=response.latitude, longitude=response.longitude
    )
    response: GetTemperatureResp = get_temperature(request)
    print(response.temperature)


def get_api_response(request: GetAPIReq) -> requests.Response:
    response = requests.get(request.api_url, params=request.params)
    return response


def get_latitude_longitude(
    request: GetLatitudeLongitudeReq,
) -> GetLatitudeLongitudeResp:
    payload = {"name": request.location}
    api_request = GetAPIReq(api_url=GEOCODING_API_URL, params=payload)
    try:
        response = get_api_response(api_request)
    except Exception as e:
        print(e, "GEOCODING Api Request failed")

    json_response = response.json()
    results = json_response["results"][0]

    lat_long_resp = GetLatitudeLongitudeResp(
        latitude=results["latitude"], longitude=results["longitude"]
    )
    return lat_long_resp


def get_temperature(request: GetTemperatureReq) -> GetTemperatureResp:
    payload = GetTemperatureModel(
        latitude=request.latitude,
        longitude=request.longitude,
        hourly="temperature_2m",
        current="temperature_2m",
        forecast_days=1,
        temperature_unit="fahrenheit",
    )

    api_request = GetAPIReq(api_url=TEMPERATURE_API_URL, params=payload.model_dump())
    response = get_api_response(api_request)

    response = response.json()
    temperature = response["current"]["temperature_2m"]
    response = GetTemperatureResp(temperature=float(temperature))
    return response


if __name__ == "__main__":
    main()
