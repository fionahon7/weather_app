import argparse
import sys
import enums
from weather_stats import WeatherStats


def create_parser():
    parser = argparse.ArgumentParser(
        description="Calculate stats for historical weather app"
    )
    subparsers = parser.add_subparsers(dest="function")

    # Days of precip
    precip_parser = subparsers.add_parser(
        "days-of-precip",
        help="Calculate average days of non zero precipitation per year for a city",
    )
    precip_parser.add_argument(
        "--city", type=str, required=True, choices=[c.value for c in enums.City]
    )

    # Max temp delta
    temp_parser = subparsers.add_parser(
        "max-temp-delta",
        help="Determine the greatest single day low to high temperature "
        "change for the designated city and time period",
    )
    temp_parser.add_argument(
        "--city", type=str, required=True, choices=[c.value for c in enums.City]
    )
    temp_parser.add_argument("--year", type=int, choices=range(2010, 2020))
    temp_parser.add_argument("--month", type=int, choices=range(1, 13))

    return parser


def main():
    parser = create_parser()
    args = parser.parse_args()

    weather_stats = WeatherStats("noaa_historical_weather_10yr.csv")

    if args.function == "days-of-precip":
        result = weather_stats.days_of_precip(args.city)
        print(result)

    if args.function == "max-temp-delta":
        if args.month is not None and args.year is None:
            print("Error: Year must be specified when month is specified.")
            sys.exit(1)

        result = weather_stats.max_temp_delta(
            city=args.city, year=args.year, month=args.month
        )
        print(result)


if __name__ == "__main__":
    main()
