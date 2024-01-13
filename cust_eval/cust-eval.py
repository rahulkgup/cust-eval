# This is a sample Python script.
import argparse
import logging

import pandas as pd
import scipy.stats as stats
from lifetimes import BetaGeoFitter
from lifetimes.utils import summary_data_from_transaction_data

# Configure logging
logging.basicConfig(level=logging.WARNING)


def predict2(args):
    df = pd.read_csv(args.input)
    # preprocess data
    df['Timestamp'] = pd.to_datetime(df['Timestamp']).dt.date

    summary = summary_data_from_transaction_data(df,
                                                 'CustomerID',
                                                 'Timestamp',
                                                 'PurchaseValue',
                                                 observation_period_end=max(df["Timestamp"]))

    # fit the BG/NBD model
    bgf = BetaGeoFitter(penalizer_coef=0.006)
    bgf.fit(summary['frequency'], summary['recency'], summary['T'])

    t = 1
    summary['predicted_purchases'] = bgf.conditional_expected_number_of_purchases_up_to_time(t, summary['frequency'],
                                                                                             summary['recency'],
                                                                                             summary['T'])
    # Perform a goodness-of-fit test, e.g., Kolmogorov-Smirnov test
    ks_statistic, p_value = stats.kstest(summary['predicted_purchases'], 'gamma',
                                         args=(bgf.params_['r'], 0, 1 / bgf.params_['alpha']))

    # Check if the distribution significantly deviates from a gamma distribution
    if p_value < 0.05:  # Adjust the p-value threshold as needed
        logging.warning(
            f"Warning: Transaction rates do not follow a gamma distribution (KS statistic = {ks_statistic:.2f}, p-value = {p_value:.2f}). Assumption (ii) may be violated.")

    pd.set_option('display.max_columns', None)  # Show all columns
    pd.set_option('display.width', 0)  # Auto-detect width

    if args.command == 'count':
        # Prediction logic for count
        output_data = summary.sort_values(by='predicted_purchases').tail(args.n)
    elif args.command == 'spend':
        # Prediction logic for spend
        output_data = summary.sort_values(by='monetary_value').tail(args.n)

    return output_data


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Customer Evaluation CLI Tool')
    parser.add_argument('command', choices=['count', 'spend'])
    parser.add_argument('-n', type=int, required=True)
    parser.add_argument('--input', required=True)
    parser.add_argument('--output', required=True)
    args = parser.parse_args()

    data = predict2(args)

    data = data.applymap(lambda x: round(x, 6))

    # Save to output CSV
    data.to_csv(args.output, index=False)
