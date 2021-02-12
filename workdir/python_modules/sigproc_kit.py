#!/usr/bin/env python3



import numpy as np
from scipy import interpolate
from scipy.optimize import curve_fit

def remove_nan(data):
  mask = ~np.isnan(data)
  return data[mask]


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


def fft_gauss_LPF(x,time_vec,**kwargs):
  delta_t = x[1]-x[0]

  sigma=kwargs.get("sigma",1)
  mu=kwargs.get("mu",0)
    
  # add padding at front and back, default 25%
  padding = kwargs.get("padding",0.25) ## by default, pad 50 % of the sample width at the back
    
  samples = len(time_vec)

  pad_samples = int(padding*samples)
    
  pad_vector = np.zeros(pad_samples)

  kernel_time = (np.arange(0,samples,1)-pad_samples)*delta_t
  kernel = gauss(kernel_time,mu=mu,sigma=sigma)


  time_vec_list = [ time_vec, kernel ]
  
  freq_vec = None
  for time_vec in time_vec_list:
    if freq_vec is None:
      freq_vec = np.fft.rfft(
          np.concatenate(
              (time_vec, pad_vector)
          )
      )
    else:
      freq_vec = freq_vec * np.fft.rfft(
          np.concatenate(
              (time_vec,pad_vector)
          ) * delta_t
      )
  
  
  out = np.fft.irfft(freq_vec)[pad_samples:samples+pad_samples]
  while (len(out) < samples):
    out = np.concatenate((out,np.array([out[-1]])),axis=None)
  
  return out  

      

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


def discriminate(time,y,thresh,hysteresis,hyst_offset):
  out = np.zeros(len(y))
  
  rising_thresh = thresh + hysteresis + hyst_offset
  falling_thresh = thresh + hyst_offset
  
  state = 1
  t1 = None
  tot = None
  
  for i in range(0,len(y)):
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

def rise_time(time,y,**kwargs):
  lo = kwargs.get("lo",0)
  hi = kwargs.get("hi",np.max(y))
  
  lo_thresh = kwargs.get("lo_thresh",hi*0.1)
  hi_thresh = kwargs.get("hi_thresh",hi*0.9)

  dummy, lo_time, dummy = discriminate(time,y,lo_thresh,0,0)
  dummy, hi_time, dummy = discriminate(time,y,hi_thresh,0,0)
  
  return (hi_time-lo_time)

def const_frac_discriminator(time,y,**kwargs):
  thresh = kwargs.get("thresh",0.2)
  dummy, t1, tot = discriminate(time,normalize_max(y),thresh,0,0)
  return (t1, tot)


def detector_signal_function(x, Q, tau1, tau2, delay):
    x_ = x - delay
    R  = 50
    return (x_ > 0) * R*Q/(tau1-tau2) *(np.exp(-x_/tau1) - np.exp(-x_/tau2))

def detector_signal_fit(time,y,**kwargs):
  ##################################################
  ##                     fit                      ##
  ##################################################
  
  show = kwargs.get("show",1)
  verbose = kwargs.get("verbose",1)

  
  xdata = time
  ydata = remove_baseline(y)
  
  # remove nan with mask
  mask = ~np.isnan(xdata) & ~np.isnan(ydata)
  xdata = xdata[mask]
  ydata = ydata[mask]
  
  
  
  p0 = kwargs.get("p0",[50e-12,5e-9,30e-9, 2e-9])
  
  popt, pcov = curve_fit(detector_signal_function, xdata, ydata, p0 = p0 )

  R     = 50
  Q     = popt[0]
  tau1  = popt[1]
  tau2  = popt[2]
  delay = popt[3]
  t_max = np.log(tau1/tau2)/((1./tau2)-(1./tau1))
  v_max = R*Q  * 1/tau1 * (tau1/tau2)**(-tau2/(tau1-tau2))

  if show:
    from matplotlib import pyplot as plt
    plt.plot(time,ydata,color="blue",label="data")
    plt.plot(xdata, detector_signal_function(xdata, *popt), 'r-',
             label="fit"
            )
    
    
    plt.xlabel("time (s)")
    plt.ylabel("signal (V)")
    plt.title("detector model fit")
    plt.xscale("linear")
    plt.legend()
    plt.show
    
  if verbose:  
    print("fit parameters:")
    print("Q     = {:3.3f} pC".format(Q*1e12))
    print("tau1  = {:3.3f} ns".format(tau1*1e9))
    print("tau2  = {:3.3f} ns".format(tau2*1e9))
    print("delay = {:3.3f} ns".format(delay*1e9))
    print("t_max = {:3.3f} ns".format(t_max*1e9))
    print("v_max = {:3.3f} mV".format(v_max*1e3))
    print()
    print("ltspice_formula:")
    print(
        "V=50*{:3.3e}/({:3.3e}-{:3.3e})*(exp(-time/{:3.3e})-exp(-time/{:3.3e}))".format(Q,tau1,tau2,tau1,tau2)
         )
    print()
    print("return (Q, tau1, tau2, delay, v_max, t_max)")
  return (Q, tau1, tau2, delay, v_max, t_max)


  
  
