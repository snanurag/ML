import pandas as pd
import numpy as np
import os
import seaborn as sns
from util import filterOnCorrelationLimit

# featuretools for automated feature engineering
import featuretools as ft

# matplotlit and seaborn for visualizations
import matplotlib.pyplot as plt


def kde_target_plot(df, feature):
    """Kernel density estimate plot of a feature colored
    by value of the target."""
    
    # Need to reset index for loc to workBU
    df = df.reset_index()
    plt.figure(figsize = (10, 6))
    plt.style.use('fivethirtyeight')
    
    # plot repaid loans
    sns.kdeplot(df.loc[df['TARGET'] == 0, feature], label = 'target == 0')
    # plot loans that were not repaid
    sns.kdeplot(df.loc[df['TARGET'] == 1, feature], label = 'target == 1')
    
    # Label the plots
    plt.title('Distribution of Feature by Target Value')
    plt.xlabel('%s' % feature); plt.ylabel('Density');
    plt.show()

feature_sample = pd.read_csv(os.path.dirname(os.path.abspath(__file__)) +'/feature_matrix_train.csv', nrows = 20000)

feature_sample = filterOnCorrelationLimit(feature_sample, 'SK_ID_CURR', 'TARGET', 0.03, -0.03)

print('Shape -> ',feature_sample.shape)
print('Most Positive Correlations:\n', correlations.tail(25))
print('\nMost Negative Correlations:\n', correlations.head(25))

# kde_target_plot(feature_sample, feature = 'MAX(bureau_CREDIT_ACTIVE_Active.DAYS_ENDDATE_FACT)')
# kde_target_plot(feature_sample, feature = 'MAX(bureau_CREDIT_ACTIVE_Active.DAYS_CREDIT)')

