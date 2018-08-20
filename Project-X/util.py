

def filterOnCorrelationLimit(df, id, target, upperlimit, lowerlimit):
    correlations = df.corr()[target].sort_values()
    for k in correlations.index:
        if correlations[k] < 0.03 and correlations[k] > -0.03 and k != id and k != target:
            # print('droping k ->', k)
            df = df.drop([k], axis=1)
    return df

