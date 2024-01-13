import pandas as pd
from lifetimes.utils import summary_data_from_transaction_data


def transform_data(csv_file):
    # Load data
    df = pd.read_csv(csv_file)
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])

    df = pd.read_csv(csv_file)
    # preprocess data
    df['Timestamp'] = pd.to_datetime(df['Timestamp']).dt.date

    summary = summary_data_from_transaction_data(df,
                                                 'CustomerID',
                                                 'Timestamp',
                                                 'PurchaseValue',
                                                 observation_period_end=max(df["Timestamp"]))

    return summary
