
import time


import requests







local_objects = {}


def screenshot():
  if ( not("ip" in local_objects)):
    raise NameError("device not initialized")
    
  ip = local_objects['ip']
  
  from IPython.display import Image

  import os
  os.system("wget 'http://{}/crt_print.bmp?lang=en' -O /dev/shm/HMP4040_{}_ssht.bmp".format(ip,ip))
  os.system("convert /dev/shm/HMP4040_{}_ssht.bmp /dev/shm/HMP4040_{}_ssht.gif".format(ip,ip))

  with open('/dev/shm/HMP4040_{}_ssht.gif'.format(ip),'rb') as f:
    display(Image(data=f.read(), format='gif'))
    
  os.system("rm /dev/shm/HMP4040_{}_ssht.bmp /dev/shm/HMP4040_{}_ssht.gif".format(ip,ip))


def init(ip):


  local_objects["ip"] = ip
  
  idn_str = identify()
  if( "HMP4040" in idn_str):
    print("successfully connected to HMP4040 at {}".format(ip))
  else:
    del local_objects["ip"]
    raise NameError("could not connect to desired device")
  
  return 1


def send_cmd(cmd,**kwargs):
  if ( not("ip" in local_objects)):
    raise NameError("device not initialized")
    
  ip = local_objects['ip']
  timeout = float(kwargs.get("timeout",0.5))
  url = 'http://'+ip+'/scpi_response.txt'

  line = ""
  for cmd_ in cmd.split("\n"):
    x = requests.get(url, params={'lang':'en', 'request':cmd_, 'cmd':'Send'}, timeout=timeout)
    line = x.text
    
  line = line.replace("\r","")
  line = line.replace("\n","")
  return line

def identify():
  return send_cmd("*IDN?")

def output_off():
  send_cmd("OUTPUT:GENERAL OFF")

def output_on():
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
  device = "hmp4040_"+local_objects['ip']
  print("device: {:s}".format(device))
  for i in range(1,5):
    print("volt {:f} curr {:f} state {:d}".format( get_volt(i), get_curr(i), get_state(i))) 
    
    