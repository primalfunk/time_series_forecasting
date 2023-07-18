import pandas as pd
from data_loader import DataLoader, DataPrep
from forecaster import Forecaster

# Set up a main function to orchestrate the entire process
def main():
    dl = DataLoader()
    dp = DataPrep(dl.load_data())
    df = dp.df
    df['Date'] = df['Date'].map(lambda x: (x - pd.Timestamp("1970-01-01")) // pd.Timedelta('1D'))
    forecaster = Forecaster()
    forecaster.fit(df)
    future_df = generate_future_dates('2023-07-30', '2023-12-31', df)
    predictions = forecaster.predict(future_df)
    predictions['Date'] = predictions['Date'].map(lambda x: pd.Timestamp("1970-01-01") + pd.Timedelta(days=int(x)))
    predictions.to_csv('predictions.csv', index=False)
    print("Forecasting process completed and predictions saved to 'predictions.csv'.")
    print(predictions.head())

# Define a function to generate future dates
def generate_future_dates(start_date, end_date, df):
    future_dates = pd.date_range(start=start_date, end=end_date, freq='W')
    
    future_dfs = []
    for name, group in df.groupby(['CustomerGroup', 'Model']):
        future_df = pd.DataFrame({'Date': future_dates, 'CustomerGroup': name[0], 'Model': name[1]})
        # Convert 'Date' to a numerical format
        future_df['Date'] = future_df['Date'].map(lambda x: (x - pd.Timestamp("1970-01-01")) // pd.Timedelta('1D'))
        
        future_dfs.append(future_df)
    
    future_df = pd.concat(future_dfs, ignore_index=True)
    return future_df

# Run the main function
if __name__ == "__main__":
    main()