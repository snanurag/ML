from parsing import data
from sklearn.preprocessing import MinMaxScaler
# progress bar
from tqdm import tqdm


def normalize(v):
    df = data[v.get('data')]
    data[v.get('data')+'_norm_factor'] = df.groupby(v.get('within-group'), as_index=False).max()
    df_norm = data[v.get('data')+'_norm_factor']
    df = df.sort_values([v.get('within-group')])
    itr_norm = df_norm.iterrows()
    cont_while = True
    try:
        val = next(itr_norm)
    except StopIteration:
        cont_while = False
    print('This may take time. Normalization is in progress........')
    for i, row in df.iterrows():
        if row[v.get('within-group')] == val[1][v.get('within-group')]:
            norm_val = row[v.get('target')] / val[1][v.get('target')]
            df.set_value(i, v.get('target'), norm_val)
        if row[v.get('within-group')] < val[1][v.get('within-group')]:
            continue
        while row[v.get('within-group')] > val[1][v.get('within-group')] and cont_while:
            try:
                val = next(itr_norm)
                if row[v.get('within-group')] == val[1][v.get('within-group')]:
                    norm_val = row[v.get('target')] / val[1][v.get('target')]
                    df.set_value(i, v.get('target'), norm_val)
            except StopIteration:
                cont_while = False
    data[v.get('data')] = df

def denormalize(v):
    denorm(v)
    if 'secondary-source' in v:
        denorm(v, v.get('secondary-source'))

def denorm(v, norm_data=None):
    df = data[v.get('data')]
    if norm_data == None:
        df_norm = data[v.get('normalized-data')+'_norm_factor']
    else:
        df_norm = data[norm_data]
    df = df.sort_values([v.get('within-group')])
    itr_norm = df_norm.iterrows()
    cont_while = True
    try:
        val = next(itr_norm)
    except StopIteration:
        cont_while = False
    print('This may take time. De-normalization is in progress........')
    for i, row in df.iterrows():
        if row[v.get('within-group')] == val[1][v.get('within-group')]:
            if row[v.get('target')] <= 1:
                denorm_val = row[v.get('target')] * val[1][v.get('target')]
            else:
                denorm_val = row[v.get('target')]
            df.set_value(i, v.get('target'), denorm_val)
        if row[v.get('within-group')] < val[1][v.get('within-group')]:
            continue
        while row[v.get('within-group')] > val[1][v.get('within-group')] and cont_while:
            try:
                val = next(itr_norm)
                if row[v.get('within-group')] == val[1][v.get('within-group')]:
                    if row[v.get('target')] <= 1:
                        denorm_val = row[v.get('target')] * val[1][v.get('target')]
                    else:
                        denorm_val = row[v.get('target')]
                    df.set_value(i, v.get('target'), denorm_val)
            except StopIteration:
                cont_while = False
    data[v.get('data')] = df
    
def normalize_scaled(value):
    for v in value:
        df = data[v.get('data')]
        scaler = MinMaxScaler(feature_range=(v.get('scale')[0], v.get('scale')[1]))
        df_grps = df.groupby(v.get('within-group'))
        for id, d in tqdm(df_grps, total=df_grps.ngroups, desc="Normalized Scale progress"):
            d = scaler.fit_transform(d[v.get('target')].values.reshape(-1, 1))
            for i, row in df.iterrows():
                df.set_value(i, v.get('target'), row[v.get('target')])

