#!/usr/bin/env python3
 
import numpy as np
import vxi11
from numpy import pi

from scipy import interpolate

import struct
from time import sleep
import sys
import os
import datetime

local_objects = {}

## change the IP address to your instrument's IP
#inst = vxi11.Instrument('TCPIP0::192.168.43.125::INSTR')
##inst = vxi11.Instrument('USB0::0x1AB1::0x0641::DG4E212801262::INSTR')
#print(session.ask('*IDN?'))

def open_session(ip):
  
  # Open socket, create waveform, send data, read back and close socket
  print("connect to device ...")
  session = vxi11.Instrument('TCPIP::{}::INSTR'.format(ip))
  session.timeout = 500
  session.clear()
  #session.chunk_size = 102400
  print("*IDN?")
  idn_str = session.ask("*idn?")
  print(idn_str)
  if( "Rigol Technologies,DG4202" in idn_str):
    print("success!")
  else:
    session.close()
    raise NameError("could not communicate with device, or not a Tektronix AWG70002A")
  local_objects["session"] = session
  local_objects["ip"] = ip
  return session
  


def close_session():
  if (not("session" in local_objects.keys())):
    raise NameError("there is no running communication session with AWG!")
  session = local_objects["session"]
  
  print("close socket")
  session.close()
  
def __del__(self):
  close_session()



def resample(target_x,data_x,data_y,**kwargs):
  idle_val = kwargs.get("idle_val",0.)
  f = interpolate.interp1d(data_x,data_y,bounds_error=False, fill_value=idle_val)
  out_x = target_x
  out_y = f(target_x)
  return (out_x,out_y)


def spice_float(argument):
   
  if( isinstance(argument,str)):
   
    expr = argument
    if("p" in expr):
      expr = expr.replace("p","e-12")
    elif("n" in expr):
      expr = expr.replace("n","e-9")
    elif("u" in expr):
      expr = expr.replace("u","e-6")
    elif("m" in expr):
      expr = expr.replace("m","e-3")
    elif("k" in expr):
      expr = expr.replace("k","e3")
    elif("Meg" in expr):
      expr = expr.replace("Meg","e6")
    elif("M" in expr):
      expr = expr.replace("M","e6")
    elif("G" in expr):
      expr = expr.replace("G","e9")
    elif("T" in expr):
      expr = expr.replace("T","e12")
      
    try:
      number = float(expr)
    except:
      raise NameError("cannot convert \"{}\" to a reasonable number".format(argument))
  else:
    number = float(argument)
  
  return number



def prefix_number(number):
  nstr = str(number)
  if number < 1e-6:
    nstr = str(number*1e9)+"N"
  elif number < 1e-3:
    nstr = str(number*1e6)+"U"
  elif number < 1e-0:
    nstr = str(number*1e3)+"M"
  return nstr
 



def my_float_str(a):
  return "{:f}".format(a)


def set_waveform(channel,data_x,data_y,**kwargs):
  if (not("session" in local_objects.keys())):
    raise NameError("there is no running communication session with AWG!")
  session = local_objects["session"]
  # example set_waveform(1,time,ampl, samples=1024)

  idle_val = kwargs.get("idle_val",0.)
  
  samples = kwargs.get("samples",2**12)
  burst   = kwargs.get("burst",True)

  #data_x = data_x - data_x[0]

  period = kwargs.get("period",data_x[-1])

  x=np.linspace(0,period,samples)

  # interpolate in case your csv time steps are not equal size,
  # for example if it is exported by LTSpice
  dummy, y = resample(x,data_x,data_y,idle_val=idle_val)
  
  
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

  
  #session.write("OUTPUT"+str(channel)+" OFF")
  session.write("SOURCE"+str(channel)+":TRACE:DATA VOLATILE,"+ val_str)
  session.write("SOURCE"+str(channel)+":VOLTAGE:UNIT VPP")
  session.write("SOURCE"+str(channel)+":VOLTAGE:LOW {:e}".format(v_low))
  session.write("SOURCE"+str(channel)+":VOLTAGE:HIGH {:e}".format(v_high))
  session.write("SOURCE"+str(channel)+":PERIOD {:e}".format(period))

  if burst:
    session.write("SOURCE"+str(channel)+":BURSt ON")
    session.write("SOURCE"+str(channel)+":BURSt:MODE TRIGgered")
    
  session.write("OUTPUT"+str(channel)+" ON")















  
def program_trace(xdata,ydata,**kwargs):
  
  if (not("session" in local_objects.keys())):
    raise NameError("there is no running communication session with AWG!")
  session = local_objects["session"]
  
  
  
  trace       = int(kwargs.get("trace",1))
  #idle_val    = spice_float(kwargs.get("idle_val",0))
  yscale      = spice_float(kwargs.get("yscale",1))
  xscale      = spice_float(kwargs.get("xscale",1))
  delay       = spice_float(kwargs.get("delay",0e-9))
  sample_rate = int(spice_float(kwargs.get("sample_rate",8e9)))
  invert      = int(kwargs.get("invert",0))
  period      = spice_float(kwargs.get("period",0))

  if(invert):
    yscale = yscale * (-1)
  
  set_waveform(trace,xdata*xscale+delay,ydata*yscale,period=period)
  
  



def pulser(**kwargs):
    
  open_ip = ""
  if "ip" in local_objects:
    open_ip = local_objects["ip"]

  trace       = int(kwargs.get("trace",1))
  on_val      = spice_float(kwargs.get("on_val",0.25))
  idle_val    = spice_float(kwargs.get("idle_val",0))
  width       = spice_float(kwargs.get("width",50e-9))
  delay       = spice_float(kwargs.get("delay",0e-9))
  sample_rate = int(spice_float(kwargs.get("sample_rate",8e9)))
  invert      = int(kwargs.get("invert",0))
  ip          = str(kwargs.get("ip",open_ip))
  period      = spice_float(kwargs.get("period",0))
  yscale      = spice_float(kwargs.get("yscale",1))
  xscale      = spice_float(kwargs.get("xscale",1))
  
  leading_edge   = spice_float(kwargs.get("leading_edge",0))
  trailing_edge  = spice_float(kwargs.get("trailing_edge",0))

  
  
  #xdata = np.arange(0,width,1./sample_rate)
  #ydata = np.ones(len(xdata))*on_val
  
  delay += leading_edge/2
  
  xlist = []
  ylist = []
  
  xlist += [-leading_edge/2]
  ylist += [idle_val]
  
  xlist += [leading_edge/2]
  ylist += [on_val]
  
  xlist += [width - trailing_edge/2]
  ylist += [on_val]
  
  xlist += [width + trailing_edge/2]
  ylist += [idle_val]
  
  
  xdata = np.array(xlist)
  ydata = np.array(ylist)
  
  open_session(ip)

  program_trace( xdata, ydata, 
                     trace       = trace,
                     idle_val    = idle_val,
                     xscale      = xscale,
                     yscale      = yscale,
                     delay       = delay,
                     invert      = invert,
                     sample_rate = sample_rate,
                     period      = period
                  )

  #awg.run()
  close_session()




 
 
 
 
 
