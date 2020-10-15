
import requests


local_objects = {}



def init(ip):


  local_objects["ip"] = ip
  
  idn_str = send_cmd("aoeiaoei")
  if( "-99 Unrecognized Command. MN:RCDAT-6000" in idn_str):
    print("successfully connected to RCDAT-6000 at {}".format(ip))
  else:
    del local_objects["ip"]
    raise NameError("could not connect to desired device")

  return 1


def send_cmd(cmd,**kwargs):
  if ( not("ip" in local_objects)):
    raise NameError("device not initialized")
    
  ip = local_objects['ip']
  timeout = float(kwargs.get("timeout",0.5))


  line = ""
  for cmd_ in cmd.split("\n"):

    
    if( "?" in cmd_):

      # the params dict is just a quick and dirty fix to force a
      # question mark in the query string
      cmd_.replace("?","")
      url = 'http://'+ip+'/'+cmd_
      x = requests.get(url,params={"a":"a"}, timeout=timeout)
      line = x.text
    else:
      url = 'http://'+ip+'/'+cmd_
      x = requests.get(url, timeout=timeout)
      line = x.text

    
  line = line.replace("\r","")
  line = line.replace("\n","")
  return line


def get_att():
  return float(send_cmd("ATT?"))

def set_att(att):
  send_cmd("SETATT={:3.3f}".format(att))
  print("new attenuation: {:3.3f} dB".format(get_att()))


    