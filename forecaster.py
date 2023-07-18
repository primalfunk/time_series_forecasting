from sklearn.linear_model import LinearRegression
import pandas as pd

class Forecaster:
    def __init__(self):
        self.models_quantity = {}
        self.models_sales = {}

    def fit(self, df):
        groups = df.groupby(['CustomerGroup', 'Model'])
        for name, group in groups:
            X = group['Date'].map(lambda x: (pd.Timestamp(x) - pd.Timestamp("1970-01-01")) // pd.Timedelta('1D')).values.reshape(-1, 1)
            y_quantity = group['Quantity'].values
            y_sales = group['Sales'].values
            model_quantity = LinearRegression()
            model_quantity.fit(X, y_quantity)
            model_sales = LinearRegression()
            model_sales.fit(X, y_sales)
            self.models_quantity[name] = model_quantity
            self.models_sales[name] = model_sales

    def predict(self, df):
        df_copy = df.copy()
        forecast_df = pd.DataFrame()

        for name, group in df_copy.groupby(['CustomerGroup', 'Model']):
            model_quantity = self.models_quantity.get(name)
            model_sales = self.models_sales.get(name)

            if model_quantity is not None and model_sales is not None:
                # Convert 'Date' to a numerical format
                forecast_dates = group['Date'].map(lambda x: (pd.Timestamp(x) - pd.Timestamp("1970-01-01")) // pd.Timedelta('1D')).values.reshape(-1, 1)
                forecast_quantity = model_quantity.predict(forecast_dates)
                forecast_sales = model_sales.predict(forecast_dates)

                predictions_df = pd.DataFrame({
                    'Date': group['Date'],
                    'CustomerGroup': name[0],
                    'Model': name[1],
                    'Forecasted Quantity': forecast_quantity,
                    'Forecasted Sales': forecast_sales
                })

                forecast_df = pd.concat([forecast_df, predictions_df])

        return forecast_df