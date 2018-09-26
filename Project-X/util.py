
from parsing import data

def filterOnCorrelationLimit(df, id, target, upperlimit, lowerlimit):
    correlations = df.corr()[target].sort_values()
    for k in correlations.index:
        if correlations[k] < 0.03 and correlations[k] > -0.03 and k != id and k != target:
            # print('droping k ->', k)
            df = df.drop([k], axis=1)
    return df

def display(v):
    for a in v:
        df = data[a.get('data')]
        if 'min' in a:
            print('Minimum %s in %s is %s' %(a.get('min'), a.get('data'),df[a.get('min')].min()))
        if 'max' in a:
            print('Maximum %s in %s is %s' %(a.get('max'), a.get('data'),df[a.get('max')].max()))

