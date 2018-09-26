from os import path
import sys,os
# from custom import custom
import parsing
from parsing import data

sys.path.append(os.getcwd())

def customize_column(arr):
    for a in arr:
        method_to_call = getattr(__import__('custom.custom', globals(), locals(), [a.get('func')]), a.get('func'))
        args = get_args(a.get('args'))
        key = 'data'
        if 'out-col' in a:
            data[a.get(key)][a.get('out-col')] = data[a.get(key)][a.get('in-col')].apply(method_to_call, args=(args))
            print('New column %s is generated for %s' % (a.get('out-col'), a.get(key)))
        else:
            data[a.get(key)][a.get('in-col')] = data[a.get(key)][a.get('in-col')].apply(method_to_call, args=(args))
            print('Column %s is customized for %s' % (a.get('in-col'), a.get(key)))

        
def customize(arr):
    custom = __import__("custom.custom")
    for a in arr:
        df = parsing.data[a.get('data')]
        args = get_args(a.get('args'))
        for c in df:
            method_to_call = getattr(custom, a.get('func'))
            df[c] = df[c].apply(method_to_call, args=(args))

def customize_row(arr):
    for a in arr:
        args = get_args(a.get('args'))
        method_to_call = getattr(__import__('custom.custom', globals(), locals(), [a.get('func')]), a.get('func'))
        data[a.get('data')] = data[a.get('data')].apply(method_to_call, axis=1, args=(args)) 

def get_args(arr):
    args =[]
    if arr is None:
        return args
    for l in arr:
        if 'data' in l:
            args.append(data[l.get('data')])
        else:
            args.append(l)
    return args

def test():
    print("test")