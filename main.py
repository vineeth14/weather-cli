import argparse
import requests
import json

# add this to a env file
GEOCODING_API_URL = "https://geocoding-api.open-meteo.com/v1/search"
TEMPERATUR_API_URL = "https://api.open-meteo.com/v1/forecast"


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    temperature_parser = subparsers.add_parser(
        "temperature", help="Get today's temperature"
    )
    temperature_parser.add_argument("city", help="name of city")

    args = parser.parse_args()

    commands = {"temperature": lambda: get_temperature(args.city)} # this should call a handler.

    command_func = commands.get(args.command)

    if command_func:
        command_func()
    else:
        parser.print_help()


def get_latitude_longitude(location: str):
    payload = {"name": location}
    response = requests.get(GEOCODING_API_URL, params=payload) # helper func
    response = response.json()
    response = response['results'][0] 

    latitude: float = response['latitude']
    longitude: float = response['longitude']
    return latitude, longitude

# this should be pure like get_latitude_longitude. and add a helper to format string
def get_temperature(location):
    latitude, longitude = get_latitude_longitude(location)
    payload = {
        "latitude": latitude,
        "longitude": longitude,
        "hourly": "temperature_2m",
        "current": "temperature_2m",
        "forecast_days": 1, # update this
        "temperature_unit": "fahrenheit",
            }
    response = requests.get(TEMPERATUR_API_URL, params=payload)
    response = response.json()
    temperature = response['current']['temperature_2m']
    print(str(temperature) + "F")
    return temperature


if __name__ == "__main__":
    main()
