
import vxi11




local_objects = {}






def init(ip):
  agilent = vxi11.Instrument('TCPIP0::{}::INSTR'.format(ip))


  agilent.timeout = 2000
  agilent.clear()
  agilent.chunk_size = 102400
  local_objects["agilent"] = agilent
  
  print("*IDN?")
  idn_str =agilent.ask("*IDN?")
  print(idn_str)
  if( "Agilent Technologies,34410A" in idn_str):
    print("successfully connected to Agilent Multimeter")
  else:
    raise NameError("could not connect to desired device")
  
  return 1





def send_cmd(cmd,**kwargs):
  if ( not("agilent" in local_objects)):
    raise NameError("device not initialized")
    
  agilent = local_objects['agilent']

  line = agilent.ask(cmd)
    
  line = line.replace("\r","")
  line = line.replace("\n","")
  return line

def identify():
  return send_cmd("*IDN?")


def read_voltage():
  return float(send_cmd("MEAS:VOLT?"))