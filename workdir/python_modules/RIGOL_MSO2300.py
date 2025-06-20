#!/usr/bin/env python3
 
import numpy as np
import vxi11
from numpy import pi
import array
import time
 



#debugging stuff, too lazy to clean up
ovrride_lofirst = False ## needed if you use lxi
ovrride_lofirst_val = False ## needed if you use lxi



local_objects = {}

def ask(string):
  if (not("scope" in local_objects.keys())):
    raise NameError("there is no running communication session with oscilloscope!\nrun init() first!")
  scope = local_objects["scope"]
  return scope.ask(string)

def read_raw():
  if (not("scope" in local_objects.keys())):
    raise NameError("there is no running communication session with oscilloscope!\nrun init() first!")
  scope = local_objects["scope"]
  return scope.read_raw()

def write(string):
  if (not("scope" in local_objects.keys())):
    raise NameError("there is no running communication session with oscilloscope!\nrun init() first!")
  scope = local_objects["scope"]
  return scope.write(string)

def init(ip):
  scope = vxi11.Instrument('TCPIP0::{}::INSTR'.format(ip))


  scope.timeout = 2000
  scope.clear()
  scope.chunk_size = 102400
  local_objects["scope"] = scope
  
  print("*IDN?")
  idn_str =scope.ask("*IDN?")
  print(idn_str)
  if( "RIGOL TECHNOLOGIES,MSO23" in idn_str):
    print("successfully connected to RIGOL scope!")
  else:
    raise NameError("could not connect to desired device")
  
  return 1




def prefix_number(number):
  nstr = str(number)
  if number < 1e-6:
    nstr = str(number*1e9)+"N"
  elif number < 1e-3:
    nstr = str(number*1e6)+"U"
  elif number < 1e-0:
    nstr = str(number*1e3)+"M"
  return nstr
    
def next_bigger_125_number(x):
  a = x
  e = 1
  if(x < 1e-6):
    a = x/1e-9
    e = 1e-9
  elif( x < 1e-3):
    a = x/1e-6
    e = 1e-6
  
  if a <= 1:
    a = 1
  elif a <= 2:
    a = 2
  elif a <= 5:
    a = 5
  elif a <= 10:
    a = 10
  elif a <= 20:
    a = 20
  elif a <= 50:
    a = 50
  elif a <= 100:
    a = 100
  elif a <= 200:
    a = 200
  elif a <= 500:
    a = 500
  elif a <= 1000:
    a = 1000
  
  return a*e


#
#def clear_all():
#  if (not("scope" in local_objects.keys())):
#    raise NameError("there is no running communication session with oscilloscope!\nrun init() first!")
#  scope = local_objects["scope"]
#  
#  scope.write(r"""vbs 'app.measure.clearall ' """)
#  scope.write(r"""vbs 'app.measure.clearsweeps ' """)
#
#
#def setup_measurement(meas_no,meas_source,meas_type):
#  if (not("scope" in local_objects.keys())):
#    raise NameError("there is no running communication session with oscilloscope!\nrun init() first!")
#  scope = local_objects["scope"]
#  
#  scope.write(r"""vbs 'app.measure.showmeasure = true ' """)
#  scope.write(r"""vbs 'app.measure.statson = true ' """)
#  scope.write(r"""vbs 'app.measure."""+meas_no+r""".view = true ' """)
#  scope.write(r"""vbs 'app.measure."""+meas_no+'.paramengine = "'  + meas_type +   r"""" ' """)
#  scope.write(r"""vbs 'app.measure."""+meas_no+'.source1 = "'      + meas_source + r"""" ' """)
#
#
#
#
#
#
#def measure_statistics(sources, n):
#  if (not("scope" in local_objects.keys())):
#    raise NameError("there is no running communication session with oscilloscope!\nrun init() first!")
#  scope = local_objects["scope"]
#  
#  first =  True
#  
#  return_dict = {}
#  
#  for source in sources:
#    return_dict[source] = np.zeros(n)
#  
#  
#  for j in range(0,n):
#    if first:
#      scope.write(r"""vbs 'app.ClearSweeps ' """)
#      
#    r = scope.ask(r"""vbs? 'return=app.acquisition.acquire( 0.1 , True )' """)
#    r = scope.ask(r"""vbs? 'return=app.WaitUntilIdle(5)' """)
#    if r==0:
#      print ("Time out from WaitUntilIdle, return = {0}".format(r))
#      
#    for source in sources:
#      return_dict[source][j] = read_measure(source)
#
#  return return_dict
#
#def read_measure(source): # p1 p2 ...
#  if (not("scope" in local_objects.keys())):
#    raise NameError("there is no running communication session with oscilloscope!\nrun init() first!")
#  scope = local_objects["scope"]
#  
#  answer = scope.ask(r"""vbs? 'return=app.measure.""" +source.lower() + r""".out.result.value' """)
#  if 'No Data Available' in answer:
#    return np.nan
#  else:
#    return float(answer)
#
#def trigger_n_times(n,**kwargs):
#  if (not("scope" in local_objects.keys())):
#    raise NameError("there is no running communication session with oscilloscope!\nrun init() first!")
#  scope = local_objects["scope"]
#  
#  clear_sweeps = kwargs.get("clear_sweeps",True)
#  # stop acquisition
#  scope.write(r"""vbs 'app.acquisition.triggermode = "stopped" ' """)
#
#  time.sleep(0.1)
#
#  # clear averaging
#  if clear_sweeps:
#    scope.write(r"""vbs 'app.ClearSweeps ' """)
#    
#  for i in range(0,n):
#    r = scope.ask(r"""vbs? 'return=app.acquisition.acquire( 0.1 , True )' """)
#    r = scope.ask(r"""vbs? 'return=app.WaitUntilIdle(5)' """)
#    if r==0:
#      print ("Time out from WaitUntilIdle, return = {0}".format(r))
#      
#def set_tdiv(tdiv):      
#  if (not("scope" in local_objects.keys())):
#    raise NameError("there is no running communication session with oscilloscope!\nrun init() first!")
#  scope = local_objects["scope"]
#  
#  scope.write("TDIV {:e}".format(tdiv))
#
#def set_trigger_delay(trdl):
#  if (not("scope" in local_objects.keys())):
#    raise NameError("there is no running communication session with oscilloscope!\nrun init() first!")
#  scope = local_objects["scope"]
#  
#  scope.write("TRDL {:e}".format(trdl))
#  
#def set_vdiv(source,vdiv):
#  if (not("scope" in local_objects.keys())):
#    raise NameError("there is no running communication session with oscilloscope!\nrun init() first!")
#  scope = local_objects["scope"]
#  
#  scope.write("{:s}:VDIV {:e}".format(source,vdiv))
#  
#def set_voffset(source,offset):
#  if (not("scope" in local_objects.keys())):
#    raise NameError("there is no running communication session with oscilloscope!\nrun init() first!")
#  scope = local_objects["scope"]
#  
#  scope.write("{:s}:OFFSET {:e}".format(source,offset))
#  
#def set_trig_source(source):
#  if (not("scope" in local_objects.keys())):
#    raise NameError("there is no running communication session with oscilloscope!\nrun init() first!")
#  scope = local_objects["scope"]
#  
#  scope.write("TRIG_SELECT edge,SR,{:s} ".format(source))

def capture_waveforms(sources,**kwargs):
  
  if (not("scope" in local_objects.keys())):
    raise NameError("there is no running communication session with oscilloscope!\nrun init() first!")
  scope = local_objects["scope"]
  average = kwargs.get("average",1)


  avg_runs = 0
  
  x = None
  y = {}
  
  for i in range(0,average):
    trigger_single()
    for source in sources:
      x,y_ = transfer_waveform(source,**kwargs)
      if avg_runs == 0:
        y[source] = y_
      else:
        y[source] += y_
    avg_runs += 1
    if ( average > 1):
      print("acquire {:d}/{:d}".format(avg_runs,average),end="\r")

  if ( average > 1):
    print("")

  for source in sources:
    y[source] /= float(average)
  
    
  return x,y

def trigger_single():
  if (not("scope" in local_objects.keys())):
    raise NameError("there is no running communication session with oscilloscope!\nrun init() first!")
  scope = local_objects["scope"]

  # single sequence
  scope.write(":TRIGGER:SWEEP SINGLE")
  # run
  scope.write(":RUN")

def transfer_waveform(source,**kwargs):
  if (not("scope" in local_objects.keys())):
    raise NameError("there is no running communication session with oscilloscope!\nrun init() first!")
  scope = local_objects["scope"]

  scope.write(":STOP")
  scope.write(":WAV:SOUR CHAN{}".format(source))
  scope.write(":WAV:MODE NORM")
  scope.write(":WAV:FORM BYTE")
  
  xinc  = scope.ask(":WAV:XINC?")
  yinc  = scope.ask(":WAV:YINC?")
  xorig = scope.ask(":WAV:XOR?")
  yorig = scope.ask(":WAV:YOR?")
  yref  = scope.ask(":WAV:YREF?")
  
  
  scope.write(":WAV:DATA?")
  data_bytes = scope.read_raw()
  
  
  data_list = []
  for i in range(11,len(data_bytes)-1):
      data_list.append(data_bytes[i])
  data = (np.array(data_list) - float(yref) - float(yorig)) * float(yinc) 
  
  time = np.arange(0,len(data),1) * float(xinc) + float(xorig)


  return (time,data)


## called if module is terminated
def __del__(self):
  if (not("scope" in local_objects.keys())):
    raise NameError("there is no running communication session with oscilloscope!\nrun init() first!")
  scope = local_objects["scope"]
  
  print("goodbye scope scope")
  scope.close()
  #rm.close()


