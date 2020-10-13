#!/usr/bin/env python3



import numpy as np
from scipy import interpolate



def remove_baseline(y,**kwargs):
  fraction = kwargs.get("fraction",0.08)
  # use first 8% of the signal to determine baseline
  return y - np.mean(y[0:int(len(y)*fraction)])

def find_baseline(y,**kwargs):
  fraction = kwargs.get("fraction",0.08)
  # use first 8% of the signal to determine baseline
  return np.mean(y[0:int(len(y)*fraction)])


def deltafunc_dt(data_x):
  delta_t = data_x[1]-data_x[0]
  
  deltafunc = np.zeros(len(data_x))
  deltafunc[0] = 1./delta_t # unit charge in delta pulse

  return deltafunc


def gauss(x, **kwargs):
  mu = kwargs.get("mu",0)
  sigma = kwargs.get("sigma",1)
  A = kwargs.get("A",1./(sigma*(2.*np.pi)**0.5)) ## default amplitude generates bell curve with area = 1
  return A*np.exp(-(x-mu)**2/(2.*sigma**2))


def resample(target_x,data_x,data_y):
  f = interpolate.interp1d(data_x,data_y,bounds_error=False, fill_value=0.)
  out_x = target_x
  out_y = f(target_x)
  return (out_x,out_y)

def normalize(data_y):
  return data_y/sum(data_y)

def normalize_max(data_y):
  return data_y/max(abs(data_y))

def normalize_dt(data_x,data_y):
  delta_t = data_x[1]-data_x[0]
  return data_y/sum(data_y)/delta_t

def integrate_dt(data_x,data_y):
  delta_t = data_x[1]-data_x[0]
  return np.cumsum(data_y)*delta_t
  
def convolve(y1,y2):
  samples = len(y1)
  return np.convolve(y1,y2)[0:samples]

def convolve_dt(x,y1,y2):
  delta_t = x[1]-x[0]
  samples = len(y1)
  return np.convolve(y1,y2*delta_t)[0:samples]

def diff_dt(x,y):
  delta_t = x[1]-x[0]
  return np.ediff1d(y,to_end=0)/delta_t

def load_and_resample(filename,target_x,**kwargs):
  dummy = np.loadtxt(filename)
  x_offset = kwargs.get("x_offset",0.0)
  
  data_x= dummy[:,0]+x_offset
  data_y= dummy[:,1]
  return resample(target_x,data_x,data_y)


def shift_vector(xs, n):
    e = np.empty_like(xs)
    if n >= 0:
        e[:n] = 0
        e[n:] = xs[:-n]
    else:
        e[n:] = 0
        e[:n] = xs[-n:]
    return e

def shift_time(data_x,data_y,tdiff):
  delta_t = data_x[1]-data_x[0]
  tdiff_samples = int(tdiff/delta_t)
  return (data_x, shift_vector(data_y,tdiff_samples))


def fft_convolve(x,time_vec_list,**kwargs):
  delta_t = x[1]-x[0]
  
  ## adds half the sample width at the back, so signal components at the right end of the sample have no effect on
  ## on the left side, remember, that the fft gives us a circular convolution
  padding = kwargs.get("padding",0.5) ## by default, pad 50 % of the sample width at the back
  samples = len(time_vec_list[0])
  pad_samples = int(padding*samples)
  pad_vector = np.zeros(pad_samples)
  
  freq_vec = None
  for time_vec in time_vec_list:
    if freq_vec is None:
      freq_vec = np.fft.rfft(np.concatenate((time_vec,pad_vector)))
    else:
      freq_vec = freq_vec * np.fft.rfft(np.concatenate((time_vec,pad_vector)) * delta_t)
  
  return np.fft.irfft(freq_vec)[0:samples]
      

def write_csv(filename,data_x,data_y):
  with open(filename,"w") as f:
    for i in range(0,len(data_x)):
      f.write("{:E}\t{:E}\n".format(data_x[i],data_y[i]))
    f.close()

def read_csv(filename):
  wav = np.loadtxt(filename)
  x = wav[:,0]
  y = wav[:,1]
  return (x,y)




#+
#|                                    example of my hystereris definition
#|
#|
#|                                                 XXXXXXX
#|                                                XX     XX
#|                                              XXX       XX
#|                             ^     +-------------------------------------------+
#|                             |               X            XX
#|        hysteresis = 10 mV   |              XX thresh = 30 mV
#|                             |     +-------------------------------------------+   +
#|                             |             X                XX                     |  hyst_offset = -4 mV
#|                             v     +-------------------------------------------+   v
#|                                         XX                   XX
#|                                        XX                     XX
#|                                       XX                       XXXX
#|                                     XXX                            XXXXXXXXX
#|                                   XXX                                       X XXXXXXXXXXXX XXXX   XXXXXXXXXXXXXX
#|                              XXXXXX                                                           XXXXX             XXX
#|
#|
#|
#|
#|                              +--------------+                  +-------------------+
#|        discriminator out                    |                  |
#|                                             +------------------+
#|
#+


def discriminate(time,y,thresh,hysteresis,hyst_offset,**kwargs):
  out = np.zeros(len(y))
  
  rising_thresh = thresh + hysteresis + hyst_offset
  falling_thresh = thresh + hyst_offset
    
  start = float(kwargs.get("start",time[0]))
  
  state = 1
  t1 = None
  tot = None
  
  for i in range(0,len(y)):
    
    if time[i] >= start:
          
      v = y[i]
    
      if state == 1: 
        if v > rising_thresh:
          state = 0
          if t1 is None:
            t1 = time[i]
      else: #state == 0
        if v < falling_thresh:
          state = 1
          if tot is None:
            tot = time[i] - t1
    
    out[i] = state
    
  if t1 is None:
    t1 = -1000
  if tot is None:
    tot = -1000
  return (out, t1, tot)
    


  
  
