#!/usr/bin/env python3


import numpy as np
from matplotlib import pyplot as plt

import os

savefig = True

t0 = 0

my_files = []

file_list = os.listdir("./") # returns list
for file in file_list:
  if ".csv" in file:
    my_files += [file]


my_files.sort()



for file in my_files:
  data = np.loadtxt(file, delimiter=",")
  x = np.array(data[:,0])
  y = np.array(data[:,1])
  if(not(t0)):
    t0 = x[0]
  plt.plot((x-t0)/60,y, label=file.replace(".csv",""))

plt.legend()
plt.xlabel("t (min)")
plt.ylabel("T (C)")
plt.title("DS18x20 Temperature Sensors")

if savefig:
  plt.savefig("plot.png")
else:
  plt.show()

  
