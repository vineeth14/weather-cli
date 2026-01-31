import argparse

from handlers.temperature import temperature_handler


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


if __name__ == "__main__":
    main()
