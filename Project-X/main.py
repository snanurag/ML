import yaml
from os import path
import warnings
import parsing
import split_merge
import shutil
import dfs
import manipulation
import user_customization
import re
warnings.filterwarnings('ignore')

configfile = ""
if path.exists(path.dirname(path.abspath(__file__))+"/.config/config.yml"):
    configfile = path.dirname(path.abspath(__file__))+"/.config/config.yml"
elif path.exists(path.dirname(path.abspath(__file__))+"/.config/config.yaml"):
    configfile = path.dirname(path.abspath(__file__))+"/.config/config.yaml"
else :
    print("No config.yml file")    

with open(configfile, 'r') as stream:
    try:
        dict = yaml.load(stream)
        print("config file is ", dict)
    except yaml.YAMLError as exc:
        print(exc)

for key, value in dict.items():
    if key == "data" :
        if 'read' in value.keys():
            data = parsing.read(value["read"])
        else:
            data = parsing.read_limited(value["read-limited"])
    if key == "ohe":
        manipulation.ohe(value)
    if key == "csv":
        parsing.to_csv(value)
    if key == "customize-cell" :
        user_customization.customize(value)
    if re.search("customize-column-cell", key, re.IGNORECASE):
        user_customization.customize_column(value)
    if re.search("customize-row", key, re.IGNORECASE):
        user_customization.customize_row(value)
    if key == "merge":
        manipulation.merge(value)
    if re.search("delete-columns", key, re.IGNORECASE):
        manipulation.delete(value)
    if key == "partition" :
        for l in value:
            for k1, v1 in l.items():
                split_merge.input_partition(v1, k1)
    if key == "dfs" :
        for l in value :
            for k, v in l.items():
                dfs.run_dfs(k, v)
# shutil.rmtree("partition")