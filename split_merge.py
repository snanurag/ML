from os import path
import os
import multiprocessing
from parsing import data

print (multiprocessing.cpu_count())
partition_path = path.dirname(path.abspath(__file__)) +'/partition/'
partition_data = {}
if path.exists(partition_path) is False:
    os.makedirs(partition_path)

def create_partition(id_list, dict, partition):
    """Creates and saves a dataset with only the users in `user_list`."""
    
    for i, ids in enumerate(id_list):
        # Make the directory
        directory = partition_path+ partition + '/%d' % i
        if os.path.exists(directory):
            continue
        else:
            os.makedirs(directory)
            for k, v in dict.items():
                part_data_subset = data[k][data[k][v].isin(ids)]
                part_data_subset.to_csv(directory+'/'+k+'.csv', index = False)
        # # Subset based on user list
        # app_subset = app[app.index.isin(id_list)].copy().reset_index()
        # bureau_subset = bureau[bureau.index.isin(id_list)].copy().reset_index()

        # # Drop SK_ID_CURR from bureau_balance, cash, credit, and installments
        # bureau_balance_subset = bureau_balance[bureau_balance.index.isin(id_list)].copy().reset_index(drop = True)
        # cash_subset = cash[cash.index.isin(id_list)].copy().reset_index(drop = True)
        # credit_subset = credit[credit.index.isin(id_list)].copy().reset_index(drop = True)
        # previous_subset = previous[previous.index.isin(id_list)].copy().reset_index()
        # installments_subset = installments[installments.index.isin(id_list)].copy().reset_index(drop = True)
        

        # # Save data to the directory
        # app_subset.to_csv('%s/app.csv' % directory, index = False)
        # bureau_subset.to_csv('%s/bureau.csv' % directory, index = False)
        # bureau_balance_subset.to_csv('%s/bureau_balance.csv' % directory, index = False)
        # cash_subset.to_csv('%s/cash.csv' % directory, index = False)
        # credit_subset.to_csv('%s/credit.csv' % directory, index = False)
        # previous_subset.to_csv('%s/previous.csv' % directory, index = False)
        # installments_subset.to_csv('%s/installments.csv' % directory, index = False)

        # if partition % 10 == 0:
        #     print('Saved all files in partition {} to {}.'.format(partition + 1, directory))


def input_partition(dict, partition_name):
    count = multiprocessing.cpu_count()
    count *= 13
    chunk_size = 0 
    for k, v in dict.items():
        if (k in data) is False:
            print("Error : No data entry by name %s is present. Please refer # " %k )
        if chunk_size == 0:
            chunk_size = len(data[k]) // count
            id_list = [list(data[k].iloc[i:i+chunk_size][v]) for i in range(0, data[k].shape[0], chunk_size)]
            create_partition(id_list, dict, partition_name)
        else:
            return


            
