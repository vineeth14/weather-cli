import argparse

from handlers.temperature import temperature_handler
from handlers.forecast import forecast_handler


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    temperature_parser = subparsers.add_parser(
        "temperature", help="Get today's temperature"
    )
    temperature_parser.add_argument("city", help="name of city")

    forecast_parser = subparsers.add_parser(
        name="forecast", help="Get a 7 day forecast"
    )
    forecast_parser.add_argument("city", help="location")

    args = parser.parse_args()

    commands = {
        "temperature": lambda: temperature_handler(location=args.city),
        "forecast": lambda: forecast_handler(location=args.city),
    }

    command_func = commands.get(args.command)

    if command_func:
        command_func()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
