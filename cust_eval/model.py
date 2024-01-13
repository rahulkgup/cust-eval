import logging

from lifetimes import BetaGeoFitter
from scipy.stats import stats


def predict(summary, command, t=1):
    bgf = BetaGeoFitter(penalizer_coef=0.006)
    bgf.fit(summary['frequency'], summary['recency'], summary['T'])
    summary['predicted_purchases']  =  bgf.conditional_expected_number_of_purchases_up_to_time(t, summary['frequency'], summary['recency'], summary['T'])
    # Perform a goodness-of-fit test, e.g., Kolmogorov-Smirnov test
    ks_statistic, p_value = stats.kstest(summary['predicted_purchases'], 'gamma',
                                         args=(bgf.params_['r'], 0, 1 / bgf.params_['alpha']))

    # Check if the distribution significantly deviates from a gamma distribution
    if p_value < 0.05:  # Adjust the p-value threshold as needed
        logging.warning(
            f"Warning: Transaction rates do not follow a gamma distribution (KS statistic = {ks_statistic:.2f}, p-value = {p_value:.2f}). Assumption (ii) may be violated.")
    if command == 'count':
        # Prediction logic for count
        summary = summary.sort_values(by='predicted_purchases')
    elif command == 'spend':
        # Prediction logic for spend
        summary = summary.sort_values(by='monetary_value')

    return summary
