import dask_run
import os
import pandas as pd
from parsing import data

# featuretools for automated feature engineering
import featuretools as ft

def run_dfs(dfs_key, dfs_value):
    for l in dfs_value:
        for k, v in l.items():
            if k == 'partition':
                for partition in v:
                    print(partition)
                    for partition_name, partition_params in partition.items():
                        dask_run.run(partition_name, partition_params)
                        # create_entrysets('0', partition_name, partition_params)

def create_entitysets(part_num, partition_name, dfs_params):
    es_dict = {}
    es = ft.EntitySet(id = partition_name)
    for target in dfs_params['target']: 
        for t_k, t_v in target.items():
            s = data[t_k].duplicated(t_v)
            df_target = pd.read_csv(os.path.dirname(os.path.abspath(__file__)) +'/partition/'+partition_name+'/'+part_num+'/'+t_k+'.csv')
            index = index_needed(t_k,t_v)
            if index == True:
                es = es.entity_from_dataframe(entity_id = t_k, dataframe = df_target, make_index = True, index = t_v)
            else:
                es = es.entity_from_dataframe(entity_id = t_k, dataframe = df_target, index = t_v)
            for frame in dfs_params['frames']:
                for f_k, f_v in frame.items():
                    index = index_needed(f_k,f_v)
                    df = pd.read_csv(os.path.dirname(os.path.abspath(__file__)) +'/partition/'+partition_name+'/'+part_num+'/'+f_k+'.csv')
                    if index == True:
                        es = es.entity_from_dataframe(entity_id = f_k, dataframe = df, make_index = True, index = f_k+'_'+f_v)
                    else:
                        es = es.entity_from_dataframe(entity_id = f_k, dataframe = df, index = f_v)
                    r = ft.Relationship(es[t_k][t_v], es[f_k][f_v])
                    es = es.add_relationships([r])
            es_dict.update({t_k: es, 'num': part_num})
    return es_dict

def run_dfs_on_ft(es_dict, partition_name, dfs_params):
    for target in dfs_params['target']:
        for t_k, t_v in target.items():
            es = es_dict[t_k]
            feature_matrix, feature_names = ft.dfs(entityset = es, target_entity = t_k, agg_primitives= dfs_params['aggregation'], max_depth = 1, features_only=False, verbose=True, chunk_size=es[t_k].df.shape[0])
            feature_matrix.to_csv(os.path.dirname(os.path.abspath(__file__)) +'/partition/'+partition_name+'/'+es_dict['num']+'/fm.csv', index=False)

def index_needed(data_set, key):
    s = data[data_set].duplicated(key)
    return s.unique().size == 2 or s.unique()[0] == True
