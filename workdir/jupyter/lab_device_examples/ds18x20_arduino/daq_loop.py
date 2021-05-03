#!/usr/bin/env python3

import time
import serial
import re
import json
from junction_temp import *


device = '/dev/ttyACM0'
baudrate = 115200

timeout = 0.1
ser = serial.Serial(device, baudrate, timeout=timeout)

alias = {}
sensors = {}

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
  for name in sensors.keys():
    f = open(name+".csv", "a")
    f.write(str(mytime))
    f.write(", ")
    f.write(str(sensors[name]))
    f.write("\n")
    f.close()


def loop():
  
  
  id = 0
  
  
  print_interval = 5
  
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
                sensors[alias[id]] = temp_C
              else: 
                sensors[id] = temp_C
    curr_time = time.time()
    if( curr_time > (last_time + print_interval)):
      alias = load_alias()
      try:
        jt = read_junction_temp()
        sensors["JNC_T1"] = jt
      except:
        print("could not read multimeter")
  
      print(json.dumps(sensors, indent=2, sort_keys=True))
      log()
      last_time = curr_time
      sensors = {}


