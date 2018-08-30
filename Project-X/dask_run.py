import dask.bag as db
from dask.distributed import Client
import os
from os import listdir
import dfs
from timeit import default_timer as timer

# Use all 8 cores
def run(dfs_key, parition_name, data):
    if parition_name is None:
        print('partition name is None')
        # TODO start from here.
    else: 
        paths = listdir(os.path.dirname(os.path.abspath(__file__)) +'/partition/'+parition_name)
    # Create a bag object
    b = db.from_sequence(paths)

    # Map entityset function
    b = b.map(dfs.create_entitysets, parition_name, data)

    # Map feature matrix function
    b = b.map(dfs.run_dfs_on_ft, dfs_key, parition_name, data)

    overall_start = timer()
    b.compute()
    overall_end = timer()

    print(f"Total Time Elapsed: {round(overall_end - overall_start, 2)} seconds.")

