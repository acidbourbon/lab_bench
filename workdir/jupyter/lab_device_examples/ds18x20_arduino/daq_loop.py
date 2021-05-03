#!/usr/bin/env python3

import time
import serial
import re
import json
#from junction_temp import *

from IPython.display import clear_output

import plot

print_interval = 10

device = '/dev/ttyACM0'
baudrate = 115200

timeout = 0.1
ser = serial.Serial(device, baudrate, timeout=timeout)


local_objects = {}
local_objects["sensors"] = {}

def load_alias():
  f = open('alias.json', 'r')
  content = json.load(f)
  f.close()
  return content

def get_chunk():
  lines = ser.readlines()
  dlines = [ line.decode().replace("\r","").replace("\n","")  for line in lines ]
  return dlines






def log():
  mytime = round(time.time())
  sensors = local_objects["sensors"]
  for name in sensors.keys():
    f = open(name+".csv", "a")
    f.write(str(mytime))
    f.write(", ")
    f.write(str(sensors[name]))
    f.write("\n")
    f.close()


def loop():
  
  
  id = 0
  
  
  
  last_time = 0
  
  alias = load_alias()
  
  while 1:
    chunk = get_chunk()
    for line in chunk:
      if "ROM" in line:
        id = line.replace("ROM = ","")
      if id:
        if "Temperature" in line:
          pattern =  re.compile("Temperature = ([0-9E+\-.]+) Celsius")
          match = re.search(pattern, line)
          if match:
            temp_C = float(match.groups()[0])
            if temp_C < 85:
              if id in alias:
                local_objects["sensors"][alias[id]] = temp_C
              else: 
                local_objects["sensors"][id] = temp_C
    curr_time = time.time()
    if( curr_time > (last_time + print_interval)):
      alias = load_alias()
#      try:
#        jt = read_junction_temp()
#        local_objects["sensors"]["JNC_T1"] = jt
#      except:
#        print("could not read multimeter")
  
      clear_output(wait=True)
      log()
      print(json.dumps(local_objects["sensors"], indent=2, sort_keys=True))
      try:
        plot.plot()
      except:
        print("could not plot")
      last_time = curr_time
      local_objects["sensors"] = {}


