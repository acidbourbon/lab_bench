#!/usr/bin/env python3
 
import numpy as np
import vxi11
from numpy import pi

from scipy import interpolate

def resample(target_x,data_x,data_y):
  f = interpolate.interp1d(data_x,data_y,bounds_error=False, fill_value=0.)
  out_x = target_x
  out_y = f(target_x)
  return (out_x,out_y)

def prefix_number(number):
  nstr = str(number)
  if number < 1e-6:
    nstr = str(number*1e9)+"N"
  elif number < 1e-3:
    nstr = str(number*1e6)+"U"
  elif number < 1e-0:
    nstr = str(number*1e3)+"M"
  return nstr
 
# change the IP address to your instrument's IP
inst = vxi11.Instrument('TCPIP0::192.168.43.125::INSTR')
#inst = vxi11.Instrument('USB0::0x1AB1::0x0641::DG4E212801262::INSTR')
print(inst.ask('*IDN?'))



def my_float_str(a):
  return "{:f}".format(a)


def set_waveform(channel,data_x,data_y,**kwargs):
  # example set_waveform(1,time,ampl, samples=1024)

  
  samples = kwargs.get("samples",2**12)
  burst   = kwargs.get("burst",True)

  data_x = data_x - data_x[0]

  period = data_x[-1]

  x=np.linspace(0,period,samples)

  # interpolate in case your csv time steps are not equal size,
  # for example if it is exported by LTSpice
  dummy, y = resample(x,data_x,data_y)
  
  
  # normalize to maximum (pos/neg) amplitude
  max_ampl = max( np.array([max(y), abs(min(y))]) )
  
  v_high = max_ampl
  v_low = -1*max_ampl
  
  
  raw_y = y
  
  if max_ampl:
    raw_y = y/max_ampl

  
  if "v_range" in kwargs:
    v_high = abs(kwargs.get("v_range",2.5))
    v_low  = -v_high
    raw_y = y/v_high
    

  
  #val_str = ",".join(map(str,raw_y))
      
  val_str = ",".join(map(str,raw_y))

  
  #inst.write("OUTPUT"+str(channel)+" OFF")
  inst.write("SOURCE"+str(channel)+":TRACE:DATA VOLATILE,"+ val_str)
  inst.write("SOURCE"+str(channel)+":VOLTAGE:UNIT VPP")
  inst.write("SOURCE"+str(channel)+":VOLTAGE:LOW {:e}".format(v_low))
  inst.write("SOURCE"+str(channel)+":VOLTAGE:HIGH {:e}".format(v_high))
  inst.write("SOURCE"+str(channel)+":PERIOD {:e}".format(period))

  if burst:
    inst.write("SOURCE"+str(channel)+":BURSt ON")
    inst.write("SOURCE"+str(channel)+":BURSt:MODE TRIGgered")
    
  inst.write("OUTPUT"+str(channel)+" ON")






 
 
 
 
 
