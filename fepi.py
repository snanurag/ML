#!/usr/bin/env python3.6


import yaml
from os import path
import os
import sys
import warnings
import parsing
import split_merge
import shutil
import dfs
import manipulation
import user_customization
import re
import regression
import decision_tree
import util
from dtree import xgboost_impl
from manipulate import alterations
import ptvsd
warnings.filterwarnings('ignore')


def main():
    if sys.argv[1] == "--debug":
        debug()

    configfile = ""
    caching = False
    if path.exists(os.getcwd()+"/.config/config.yml"):
        configfile = os.getcwd()+"/.config/config.yml"
    elif path.exists(os.getcwd()+"/.config/config.yaml"):
        configfile = os.getcwd()+"/.config/config.yaml"
    else :
        print("No config.yml file")    

    with open(configfile, 'r') as stream:
        try:
            dict = yaml.load(stream)
            print("config file is parsed successfully.")
        except yaml.YAMLError as exc:
            print(exc)

    for k in dict:
        if k == 'cache':
            if dict.get(k) == True:
                caching = True
                break
            if dict.get(k) == False:
                if path.exists(parsing.cache_path):
                    shutil.rmtree(parsing.cache_path)

    for key, value in dict.items():
        if caching == True:
            if path.exists(parsing.cache_path) == False and key == 'cache':
                parsing.cache_data()
                caching = False
            elif path.exists(parsing.cache_path):
                if key != 'cache':
                    continue
                else:
                    caching = False
                    parsing.read_from_cache()

        if key == "data" :
            if 'read' in value.keys():
                data = parsing.read(value["read"])
            else:
                data = parsing.read_limited(value["read-limited"])
        if re.search("concat", key, re.IGNORECASE):
            manipulation.concat(value)
        if re.search("copy-data", key, re.IGNORECASE):
            parsing.copy(value)
        if re.search("csv", key, re.IGNORECASE):
            parsing.to_csv(value)
        if re.search("customize-cells", key, re.IGNORECASE):
            user_customization.customize(value)
        if re.search("customize-column", key, re.IGNORECASE):
            user_customization.customize_column(value)
        if re.search("customize-row", key, re.IGNORECASE):
            user_customization.customize_row(value)
        if re.search("delete-columns", key, re.IGNORECASE):
            manipulation.delete(value)
        if re.search("delete-df", key, re.IGNORECASE):
            parsing.delete_df(value)
        if re.search("delete-rows", key, re.IGNORECASE):
            manipulation.delete_row(value)
        if key.lower().startswith(("de-normalize")):
            alterations.denormalize(value)
        if re.search("display", key, re.IGNORECASE):
            util.display(value)
        if re.search("fillna-by-search", key, re.IGNORECASE):
            manipulation.fillna_by_search(value)
        elif re.search("fillna-by-mean", key, re.IGNORECASE):
            manipulation.fillna_by_mean(value)
        elif re.search("fillna", key, re.IGNORECASE):
            manipulation.fillna(value)
        if re.search("generate-column", key, re.IGNORECASE):
            user_customization.customize_column(value)
        if re.search("group-by", key, re.IGNORECASE):
            manipulation.group_by(value)
        if re.search("lightgbm", key, re.IGNORECASE):
            decision_tree.train(value)
        if re.search("merge", key, re.IGNORECASE):
            manipulation.merge(value)
        if key.lower().startswith(("normalize")):
            alterations.normalize(value)
        if re.search("ohe", key, re.IGNORECASE):
            manipulation.ohe(value)
        if re.search("partition", key, re.IGNORECASE):                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 
            for l in value:
                for k1, v1 in l.items():
                    split_merge.input_partition(v1, k1)
        if re.search("dfs", key, re.IGNORECASE):
            for l in value :
                for k, v in l.items():
                    dfs.run_dfs(k, v)
        if re.search("keras", key, re.IGNORECASE):
            regression.train(value)
        if re.search("transfer", key, re.IGNORECASE):
            manipulation.transfer(value)
        if re.search('xgboost', key, re.IGNORECASE):
            xgboost_impl.train(value)
        
# shutil.rmtree("partition")

# def caching_operation():
#     if path.exists(parsing.cache_path):
#         parsing.read_from_cache()
#     else:
#         parsing.cache_data()

def debug():
    host = "0.0.0.0"
    port = "5678"
    if len(sys.argv) > 2:
        host = sys.argv[2]
    if len(sys.argv) > 3:
        port = sys.argv[3]    
    ptvsd.enable_attach(address=(host,port))
    ptvsd.wait_for_attach()


if __name__ == '__main__':
    main()