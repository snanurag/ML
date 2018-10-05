import matplotlib
import numpy as np
import matplotlib.pyplot as plt

from parsing import data

def plot(v):
    for a in v:
        plt.rcParams['agg.path.chunksize'] = 100000
        df = data[a.get('data')]
        y = df[a.get('y')]
        x = df[a.get('x')]
        plt.ylabel(a.get('y'))
        plt.xlabel(a.get('x'))
        plt.plot(x,y, 'ro', ms=.002)
        plt.show()
        print('Plot is generated')
    