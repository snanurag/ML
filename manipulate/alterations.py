from parsing import data

def normalize(v):
    df = data[v.get('data')]
    data[v.get('data')+'_norm_factor'] = df.groupby(v.get('group-on'), as_index=False).max()
    df_norm = data[v.get('data')+'_norm_factor']
    df = df.sort_values([v.get('group-on')])
    itr_norm = df_norm.iterrows()
    cont_while = True
    try:
        val = next(itr_norm)
    except StopIteration:
        cont_while = False
    print('This may take time. Normalization is in progress........')
    for i, row in df.iterrows():
        if row[v.get('group-on')] == val[1][v.get('group-on')]:
            norm_val = row[v.get('target')] / val[1][v.get('target')]
            df.set_value(i, v.get('target'), norm_val)
        if row[v.get('group-on')] < val[1][v.get('group-on')]:
            continue
        while row[v.get('group-on')] > val[1][v.get('group-on')] and cont_while:
            try:
                val = next(itr_norm)
                if row[v.get('group-on')] == val[1][v.get('group-on')]:
                    norm_val = row[v.get('target')] / val[1][v.get('target')]
                    df.set_value(i, v.get('target'), norm_val)
            except StopIteration:
                cont_while = False
    data[v.get('data')] = df

def denormalize(v):
    df = data[v.get('data')]
    df_norm = data[v.get('normalized-data')+'_norm_factor']
    df = df.sort_values([v.get('group-on')])
    itr_norm = df_norm.iterrows()
    cont_while = True
    try:
        val = next(itr_norm)
    except StopIteration:
        cont_while = False
    print('This may take time. De-normalization is in progress........')
    for i, row in df.iterrows():
        if row[v.get('group-on')] == val[1][v.get('group-on')]:
            denorm_val = row[v.get('target')] * val[1][v.get('target')]
            df.set_value(i, v.get('target'), denorm_val)
        if row[v.get('group-on')] < val[1][v.get('group-on')]:
            continue
        while row[v.get('group-on')] > val[1][v.get('group-on')] and cont_while:
            try:
                val = next(itr_norm)
                if row[v.get('group-on')] == val[1][v.get('group-on')]:
                    denorm_val = row[v.get('target')] * val[1][v.get('target')]
                    df.set_value(i, v.get('target'), denorm_val)
            except StopIteration:
                cont_while = False
    data[v.get('data')] = df
    