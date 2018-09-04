from os import path
from custom import custom
import parsing
from parsing import data

def customize_column(arr):
    for a in arr:
        method_to_call = getattr(custom, a.get('func'))
        args = get_args(a.get('args'))
        if 'output' in a.keys():
            data[a.get('data')][a.get('output')] = data[a.get('data')][a.get('input')].apply(method_to_call, args=(args))
        else:
            data[a.get('data')][a.get('input')] = data[a.get('data')][a.get('input')].apply(method_to_call, args=(args))

def customize(arr):
    for a in arr:
        df = parsing.data[a.get('data')]
        args = get_args(a.get('args'))
        for c in df:
            method_to_call = getattr(custom, a.get('func'))
            df[c] = df[c].apply(method_to_call, args=(args))

def customize_row(arr):
    for a in arr:
        args = get_args(a.get('args'))
        method_to_call = getattr(custom, a.get('func'))
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