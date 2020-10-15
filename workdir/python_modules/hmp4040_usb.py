
import time

import serial

from hameg_trb import *

device = '/dev/ttyUSB_HAMEG_LV'
baudrate = 9600


def send_cmd(cmd,**kwargs):
  timeout = float(kwargs.get("timeout",0.2))

  with serial.Serial(device, baudrate, timeout=timeout) as ser:
    ser.write(str.encode(cmd)+b"\r\n")
    line = ser.readline().decode()
    ser.close()
    line = line.replace("\r","")
    line = line.replace("\n","")
    return line

def identify():
  return send_cmd("*IDN?")

def all_off():
  send_cmd("OUTPUT:GENERAL OFF")

def all_on():
  send_cmd("OUTPUT:GENERAL ON")

def get_volt(channel):
  return float(send_cmd("INST OUT{:d}\nMEAS:VOLT?".format(channel)))

def set_volt(channel,volt):
  send_cmd("INST OUT{:d}\nVOLT {:3.3f}".format(channel,volt))

def set_curr(channel,curr):
  send_cmd("INST OUT{:d}\nCURR {:3.3f}".format(channel,curr))

def get_curr(channel):
  return float(send_cmd("INST OUT{:d}\nMEAS:CURR?".format(channel)))

def get_state(channel):
  return int(send_cmd("INST OUT{:d}\nOUTP:STATE?".format(channel)))

def set_state(channel,state):
  send_cmd("INST OUT{:d}\nOUTP:STATE {:d}".format(channel,state))

def report():
  print("device: {:s}".format(device))
  for i in range(1,5):
    print("volt {:f} curr {:f} state {:d}".format( get_volt(i), get_curr(i), get_state(i))) 
    
    