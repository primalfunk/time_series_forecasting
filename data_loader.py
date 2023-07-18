from no_share import NoShare
import pandas as pd

class DataLoader:
    def __init__(self):
        self.filepath = "excel_docs/test.csv"

    def load_data(self):
        df = pd.read_csv(self.filepath)
        return df

class DataPrep:
    def __init__(self, df):
        self.df = df
        no_share = NoShare()
        self.customers_to_filter = no_share.customers_to_filter
        self.customer_groups = no_share.customer_groups
        self.cols_to_drop = no_share.cols_to_drop
        self.preprocess()

    def preprocess(self):
        print(self.df.columns)
        self.df["Date"] = pd.to_datetime(self.df["Date"])  
        self.df['Quantity'] = self.df['Quantity'].str.replace(',', '').astype(float).round(2)
        self.df['Sales'] = self.df['Sales'].str.replace(',', '').astype(float).round(2)
        self.df.drop(self.cols_to_drop, axis=1, inplace=True)
        print(self.df.columns)
        self.df = self.df[~self.df["Customer"].isin(self.customers_to_filter)]
        self.df["CustomerGroup"] = self.df["Customer"].apply(lambda x: self.customer_groups.get(x, "Other"))
        self.df = self.df[self.df['Document Type'] == 'Invoice']
        # Drop the 'Customer' and 'Document Type' columns
        self.df.drop(['Customer', 'Document Type'], axis=1, inplace=True)
        
        # Convert 'Date' index to represent weeks, and group by 'CustomerGroup' and 'Model' 
        weekly_df = (self.df.groupby([pd.Grouper(key='Date', freq='W'), 'CustomerGroup', 'Model'])
                            .agg({'Quantity': 'sum', 'Sales': 'sum'}))
        # Reset index so 'Date' becomes a column again
        weekly_df.reset_index(inplace=True)
        self.df = weekly_df
        return None
