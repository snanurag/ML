#!/usr/bin/env python3
from contextlib import ExitStack
from functools import partial

print("counting")
with ExitStack() as stack:
    for i in range(10):
        a = i
        stack.callback(partial(print, a, i))

    x = 42
    a = x
    print("done")
print("after with")