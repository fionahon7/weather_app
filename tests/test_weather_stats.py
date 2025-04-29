import pandas as pd
import pytest
from weather_stats import WeatherStats


class MockWeatherStats(WeatherStats):
    def __init__(self):
        data = {
            "date": pd.to_datetime(
                ["2010-01-01", "2010-01-15", "2010-02-01", "2011-01-10", "2011-01-25"]
            ),
            "name": ["miami", "juneau", "boston", "boston", "boston"],
            "prcp": [0.5, 0.0, 1.2, 0.3, 0.0],
            "snow": [0.0, 1.5, 0.0, 0.0, 0.8],
            "tmin": [20.0, 10.0, 15.0, 12.0, 8.0],
            "tmax": [35.0, 30.0, 35.0, 28.0, 22.0],
            "year": [2010, 2010, 2010, 2011, 2011],
            "month": [1, 1, 2, 1, 1],
        }
        self.data = pd.DataFrame(data)


def test_days_of_precip(mocker):
    weather_stats = MockWeatherStats()
    mock_precip_data = {
        "year": [2010, 2011, 2011],
        "prcp": [1.2, 0.3, 0.0],
        "snow": [0.0, 0.0, 0.8],
    }
    mock_df = pd.DataFrame(mock_precip_data)

    mock_filter = mocker.patch("weather_stats.WeatherStats.filter_for_city")
    mock_filter.return_value = mock_df

    expected = 1.5
    actual = weather_stats.days_of_precip(city="bos")
    assert expected == actual


@pytest.mark.parametrize(
    "year, month, expected",
    [
        (None, None, 20.0),
        (2011, None, 16.0),
        (2011, 1, 16.0),
    ],
)
def test_max_temp_delta(mocker, year, month, expected):
    weather_stats = MockWeatherStats()
    mock_temp_data = {
        "date": pd.to_datetime(["2010-02-01", "2011-01-10", "2011-01-25"]),
        "tmin": [15.0, 12.0, 8.0],
        "tmax": [35.0, 28.0, 22.0],
        "year": [2010, 2011, 2011],
        "month": [2, 1, 1],
    }
    mock_df = pd.DataFrame(mock_temp_data)

    mock_filter = mocker.patch("weather_stats.WeatherStats.filter_for_city")
    mock_filter.return_value = mock_df

    actual = weather_stats.max_temp_delta(city="bos", year=year, month=month)
    assert expected == actual
