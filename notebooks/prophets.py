from typing import Optional

import pandas as pd
from prophet import Prophet

class InvalidTimeSeriesIndexException(Exception):
    """Exception raised when the DataFrame does not have a timeseries index."""

    def __init__(self, message: str = "DataFrame does not have a timeseries index.") -> None:
        self.message: str = message
        super().__init__(self.message)


def check_timeseries_index(transactions: pd.DataFrame) -> None:
    """
    Check if the DataFrame has a time series index.

    Parameters:
    - transactions (pd.DataFrame): The DataFrame to check.

    Raises:
    - InvalidTimeSeriesIndexException: If the DataFrame does not have a DatetimeIndex.
    """
    if not isinstance(transactions.index, pd.DatetimeIndex):
        raise InvalidTimeSeriesIndexException()

class ProphetModelBuilder:
    def __init__(
        self,
        data: pd.DataFrame,
        target_column: str,
        exog_columns: Optional[list[str]] = None,
        yearly_seasonality: bool = False,
        weekly_seasonality: bool = False,
        daily_seasonality: bool = False,
    ):
        check_timeseries_index(data)
        self.data = data
        self.target_column = target_column
        self.exog_columns = exog_columns
        self.yearly_seasonality = yearly_seasonality
        self.weekly_seasonality = weekly_seasonality
        self.daily_seasonality = daily_seasonality
        self.model = self._build_model()
        self.changepoints = self.model.changepoints

    def _prepare_data_for_prophet(self) -> pd.DataFrame:
        """
        Prepare the DataFrame for Prophet by renaming columns and adding exogenous variables.

        Returns:
            pd.DataFrame: DataFrame prepared for Prophet.
        """
        self.data.index.name = "ds"
        prophet_df = self.data.reset_index().rename(columns={self.target_column: "y"})

        if self.exog_columns:
            for exog in self.exog_columns:
                prophet_df = prophet_df.rename(columns={exog: f"add_{exog}"})

        return prophet_df

    def _build_model(self) -> Prophet:
        """
        Build the Prophet model for forecasting.

        Returns:
            Prophet: Fitted Prophet model.
        """
        prophet_df = self._prepare_data_for_prophet()
        model = Prophet(
            yearly_seasonality=self.yearly_seasonality,
            weekly_seasonality=self.weekly_seasonality,
            daily_seasonality=self.daily_seasonality,
        )

        if self.exog_columns:
            for exog in self.exog_columns:
                model.add_regressor(f"add_{exog}")

        model.fit(prophet_df)
        self.changepoints = model.changepoints
        return model

    def generate_forecasts(self, forecast_periods: int) -> pd.DataFrame:
        """
        Generate forecasts using the stored model.

        Parameters:
            forecast_periods (int): Number of periods to forecast.

        Returns:
            pd.DataFrame: Forecasted values.
        """
        future = self.model.make_future_dataframe(
            periods=forecast_periods, freq=self.data.index.freq or "D"
        )

        if self.exog_columns:
            for exog in self.exog_columns:
                future[f"add_{exog}"] = self.data[exog].values[-1]

        forecast = self.model.predict(future)
        return forecast[["ds", "yhat"]]

    def generate_confidence_intervals(self, forecast_periods: int) -> pd.DataFrame:
        """
        Generate confidence intervals for the forecasts.

        Parameters:
            forecast_periods (int): Number of periods to forecast.

        Returns:
            pd.DataFrame: DataFrame with 'lower_bound' and 'upper_bound' columns.
        """
        future = self.model.make_future_dataframe(
            periods=forecast_periods, freq=self.data.index.freq or "D"
        )

        if self.exog_columns:
            for exog in self.exog_columns:
                future[f"add_{exog}"] = self.data[exog].values[-1]

        forecast = self.model.predict(future)
        conf_int = forecast[["ds", "yhat_lower", "yhat_upper"]]
        conf_int = conf_int.rename(
            columns={"yhat_lower": "lower_bound", "yhat_upper": "upper_bound"}
        )

        return conf_int