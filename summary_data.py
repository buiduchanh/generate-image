import os 
import glob
import numpy as np
import matplotlib.pyplot as plt
a = {}
with open ('texts/final_add_old.txt','r') as f_ :
    lines = f_.readlines()
    for line in lines:
        length = len(line.strip())
        if length in a.keys():
            a[length] += 1
        else:
            a[length] = 1
print(a)
key_ = np.zeros(len(a))
number = np.zeros(len(a))
for idx, key in enumerate(a.keys()):
    key_[idx] += int(key)
    number[idx] += int(a[key])

print(key_)
print(number)

plt.figure(1)
plt.plot(key_, number)
plt.show()