import pandas as pd
import enums


class WeatherStats:
    """Class to load an input fie containing NOAA weather data and calculate basic stats"""

    def __init__(self, input_file: str) -> None:
        self.raw_data: pd.DataFrame = self._load_weather_data(input_file=input_file)
        self.data: pd.DataFrame = self.preprocess_data()

    def _load_weather_data(self, input_file: str) -> pd.DataFrame:
        df = pd.read_csv(input_file)
        return df

    def preprocess_data(self) -> pd.DataFrame:
        """Preprocesses weather data by stripping whitespace and converting cols
        to their appropriate types

        Returns:
            pd.DataFrame: processed weather dataframe
        """
        # Convert column names to lowercase
        self.data = self.raw_data.copy()
        self.data.columns = self.data.columns.str.lower()

        # Converting name column to lowercase
        self.data["name"] = self.data["name"].str.lower()

        for col in self.data.columns:
            # Stripping whitespace
            if self.data[col].dtype == "object":
                self.data[col] = self.data[col].str.strip()

                # Try to convert column to numeric
                try:
                    self.data[col] = self.data[col].astype(float)
                except ValueError:
                    pass

        # Fill na values with 0 for precipitation, snow, snow depth
        fillna_cols = ["prcp", "snow"]
        self.data[fillna_cols] = self.data[fillna_cols].fillna(0)

        # Date preprocessing
        self.data["date"] = pd.to_datetime(self.data["date"])
        self.data["year"] = self.data["date"].dt.year
        self.data["month"] = self.data["date"].dt.month

        return self.data

    def filter_for_city(self, city: str) -> pd.DataFrame:
        """Filter the dataframe for all rows containing the input city.

        Args:
            city (str): city name

        Returns:
            pd.DataFrame: dataframe for a given city
        """
        city_enum = enums.City.from_string(city)
        city_df = self.data[
            self.data["name"].str.contains(city_enum.full_name, na=False)
        ]

        if len(city_df) == 0:
            raise ValueError(f"City data for ({city}) not found in weather data")
        return city_df

    def days_of_precip(self, city: str) -> float:
        """Calculate the average number of days per year the given city had non-zero precipitation (either
        snow or rain) based on the entire 10 year period

        Args:
            city (str): city to evaluate
        Returns:
            float: average days of precipitation per year in the given city
        """
        city_df = self.filter_for_city(city=city)

        city_df = city_df.assign(
            non_zero_precip=(city_df["prcp"] > 0) | (city_df["snow"] > 0)
        )
        precip_days_by_year = city_df.groupby("year")["non_zero_precip"].sum()
        avg_precip_days = precip_days_by_year.mean()
        return float(avg_precip_days)

    def max_temp_delta(self, city: str, year: int = None, month: int = None) -> float:
        """Determine the greatest single day low to high temperature change for the designated city and
        time period (all time, yearly, monthly)

        Args:
            city (str): city to evalute
            year (int, optional): restrict search to a particular year
            month (int, optional): restrict search to a particular month (year is also required)

        Returns:
            float: temperature delta
        """
        city_df = self.filter_for_city(city=city)

        if year is not None:
            city_df = city_df[city_df["date"].dt.year == year]

            if month is not None:
                city_df = city_df[city_df["date"].dt.month == month]

        city_df = city_df.assign(temp_delta=city_df["tmax"] - city_df["tmin"])

        max_delta = city_df["temp_delta"].max()
        return float(max_delta)
