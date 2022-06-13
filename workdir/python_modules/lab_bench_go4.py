import os
import subprocess
import time
import signal

go4_ana_dir = "/workdir/jupyter/lab_bench_go4"
calib_file="Go4AutoSave.root_calib"

def syscall(string):
  print(string)
  answer = os.popen(string+" 2>&1").read()
  print(answer)
  return answer


def go4_recompile():
  os.chdir(go4_ana_dir)
  syscall("make clean; make")


def go4_calib(**kwargs):
    
  verbose = kwargs.get("verbose",False)
  outfile = kwargs.get("outfile","dummy.root")
  stream  = kwargs.get("stream","x86l-16")
    
  os.chdir(go4_ana_dir)

  # this tells Go4 to make a new calib
  print("make new calibration")
  syscall("cp set_TamexControl.C_newCalib set_TamexControl.C")

  syscall("rm Go4AutoSave*")
    
  go4_cmd  = "go4analysis -stream {} -outevt-class TTamex_FullEvent -enable-store -store {} -rate".format(stream,outfile)

  print(go4_cmd)
  proc = subprocess.Popen(go4_cmd, stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid) 
  while True:
    line = proc.stdout.readline().decode()
    if line:
      if verbose:
        print(line.rstrip())
      if "calibration finished" in line:
        print("calibration finished")
        break
    else:
      time.sleep(0.1)
  #proc.kill()
  os.killpg(os.getpgid(proc.pid), signal.SIGINT)
  time.sleep(3)
  os.killpg(os.getpgid(proc.pid), signal.SIGTERM)
  syscall("mv Go4AutoSave.root Go4AutoSave.root_calib")
  syscall("rm {}".format(outfile))
  if (os.path.exists(calib_file) == False):
    raise NameError("calib file {} could not be created".format(calib_file))
    
  print("success: calib file {} was created".format(calib_file))
    
      

def go4_take_data(**kwargs):

  verbose = kwargs.get("verbose",False)
  outfile = kwargs.get("outfile","new.root")
  timeout = kwargs.get("timeout",10)
  stream  = kwargs.get("stream","x86l-16")
    
  os.chdir(go4_ana_dir)


  if (os.path.exists(calib_file) == False):
    raise NameError("calib file {} does not exist!".format(calib_file))
  syscall("rm {}".format(outfile))

  # this tells Go4 to reuse an existing calib
  print("reuse existing calibration")
  syscall("cp set_TamexControl.C_reuseCalib set_TamexControl.C")
  # get the pristine calibration file, overwrite the old AutoSave
  syscall("cp {} Go4AutoSave.root".format(calib_file))
    
  go4_cmd  = "go4analysis -stream {} -outevt-class TTamex_FullEvent -enable-store -store {} -rate".format(stream,outfile)

  print(go4_cmd)

  proc = subprocess.Popen(go4_cmd, stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid) 

  while True:
    line = proc.stdout.readline().decode()
    if line:
      if verbose:
        print(line.rstrip())
      if "calibration finished" in line:
        break
    else:
      time.sleep(0.1)
  print("taking data for {:3.3f} seconds".format(timeout))
  time.sleep(timeout)
  #proc.kill()
  os.killpg(os.getpgid(proc.pid), signal.SIGINT)
  time.sleep(3)
  os.killpg(os.getpgid(proc.pid), signal.SIGTERM)
  if (os.path.exists(outfile) == False):
    raise NameError("calib file {} could not be created".format(outfile))
  print("... done. Data written to file {}".format(outfile))
