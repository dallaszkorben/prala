from itertools import islice
import numpy as np

lst = [0, 0, 1, 0, 0, 0, 1]


print(len(lst)-len("".join(map(str, lst)).rstrip("0")))

