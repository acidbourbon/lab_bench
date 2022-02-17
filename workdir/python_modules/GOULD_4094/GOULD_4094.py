#!/usr/bin/env python3


import numpy as np
import os
import glob

module_dir = "/workdir/jupyter/python_modules/GOULD_4094/"

def capture(trace,**kwargs):
    
  baudrate = kwargs.get("baudrate", 9600)
  device = kwargs.get("device","/dev/ttyUSB0")
    
  data_dir = module_dir+"/capture/" 
  os.system("rm {:s}/*".format(data_dir))
  print("communicating with scope")
  print("may take up to 15 seconds")
  output=os.popen("cd {:s}; ./dsocmd.pl -tty {:s} -capture {:s}".format(module_dir,device,trace)).read()
  print(output)

  file_list = glob.glob(data_dir+"*.dat")
  print("file list:")
  print(file_list)
  data_file = file_list[0]
  data = np.loadtxt(data_file, delimiter="\t")
  os.system("rm {:s}/*".format(data_dir))
  xdata = data[:,0]
  ydata = data[:,1]
  return xdata, ydata