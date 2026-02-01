import argparse
import asyncio

from handlers.temperature import temperature_handler
from handlers.forecast import forecast_handler
from handlers.compare import compare_handler


async def main():
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

    compare_parser = subparsers.add_parser(
        name="compare", help="Compare multiple cities"
    )
    compare_parser.add_argument(
        "cities", nargs="+", help="Add multiple cities to compare weather"
    )

    args = parser.parse_args()

    commands = {
        "temperature": lambda: temperature_handler(location=args.city),
        "forecast": lambda: forecast_handler(location=args.city),
        "compare": lambda: compare_handler(cities=args.cities),
    }

    command_func = commands.get(args.command)

    if command_func:
        await command_func()
    else:
        parser.print_help()


if __name__ == "__main__":
    asyncio.run(main())
