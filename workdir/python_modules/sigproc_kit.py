#!/usr/bin/env python3



import numpy as np
from scipy import interpolate
from scipy.optimize import curve_fit


def dB(x):
    return 20*np.log10(x)


def square_pulse(x,**kwargs):

  on_val      = float(kwargs.get("on_val",1))
  idle_val    = float(kwargs.get("idle_val",0))
  width       = float(kwargs.get("width",1))
  delay       = float(kwargs.get("delay",1))
  invert      = int(kwargs.get("invert",0))
  
  
  yscale      = float(kwargs.get("yscale",1))
  xscale      = float(kwargs.get("xscale",1))
  
  leading_edge   = float(kwargs.get("leading_edge",0))
  trailing_edge  = float(kwargs.get("trailing_edge",0))

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
  
  
  xdata = np.array(xlist) + delay
  ydata = np.array(ylist)
    
  dummy, y = resample(x,xdata,ydata,fill_value=idle_val)
  return y
  


def RC_filter(t,y,R,C,**kwargs):
  n = int(kwargs.get("n",1));
  ir = 1/(R*C)*np.exp(-t/(R*C))
  conv_list = [y] + n*[ir]
  return fft_convolve(t,conv_list)

def CR_filter(t,y,R,C,**kwargs):
  n = int(kwargs.get("n",1));
  ir = deltafunc_dt(t) - 1/(R*C)*np.exp(-t/(R*C))
  conv_list = [y] + n*[ir]
  return fft_convolve(t,conv_list)

def PZ_filter(t,y,**kwargs):
  C  = float(kwargs.get("C",1));
  R1 = float(kwargs.get("R1",1)); # the one parallel to the C
  R2 = float(kwargs.get("R2",1)); # the one to GND
  
  tau1 = float(kwargs.get("tau1",R1*C));
  tau2 = float(kwargs.get("tau2",(R1*R2)/(R1+R2)*C));
    
  ir = deltafunc_dt(t) - (tau1-tau2)/(tau1*tau2)*np.exp(-t/tau2)
  conv_list = [y] + [ir]
  return fft_convolve(t,conv_list)

def ZP_filter(t,y,**kwargs):
  C  = float(kwargs.get("C",1));
  R1 = float(kwargs.get("R1",1)); # the one parallel to the C
  R2 = float(kwargs.get("R2",1)); # the one to GND
  
  tau1 = float(kwargs.get("tau1",R2*C));
  tau2 = float(kwargs.get("tau2",(R1+R2)*C));
    
  ir = (tau1/tau2) * (deltafunc_dt(t) - (tau1-tau2)/(tau1*tau2)*np.exp(-t/tau2))
  conv_list = [y] + [ir]
  return fft_convolve(t,conv_list)

def add_noise(t,y,**kwargs):
  rms = kwargs.get("rms",1)
  bw    = kwargs.get("bw",0)
    
  sampling_freq = 1/t[1]-t[0]
  # half the sampling rate is max frequency
  # of the "sterile" gaussian noise
  noise = np.random.normal(size=len(t))

  
  if (bw != 0):
    # by RC filtering we lose amplitude
    # so we introduce makeup gain to
    # compensate for the part of the spectrum
    # that was lost
    
    gain = np.sqrt(sampling_freq/2 * 1/bw)
    
    # single pole RC brick wall equivalent
    R = 1
    C = 1/(bw*4*R)
    
    noise = gain * RC_filter(t,noise,R,C)

  return y+rms*noise

def nth_edge_time(t,y,n):
  counter = -1
  last_state = 0
  for i in range(0,len(t)):
    state = y[i]
    if ((last_state <= 0.5) and (state > 0.5)):
      counter += 1
    last_state = state
    if (counter >= n):
      return t[i]

def remove_nan(data):
  mask = ~np.isnan(data)
  return data[mask]

def sqwave(x):
  return 2*((np.ceil(x/np.pi)%2)-0.5)

def rampwave(x):
  return -1 + x/np.pi

def invrampwave(x):
  return 1 - x/np.pi

def triwave(x):
    
  return (x < np.pi/2)*(2*x/np.pi) \
       + (x >= np.pi/2)*(x < 3./2*np.pi)*(1-(x-np.pi/2)/(np.pi/2)) \
       + (x >= 3./2*np.pi)*(-1+(x-3./2.*np.pi)/(np.pi/2))

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


def resample(target_x,data_x,data_y,**kwargs):
  fill_value = float(kwargs.get("fill_value",0))
  f = interpolate.interp1d(data_x,data_y,bounds_error=False, fill_value=fill_value)
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
    if n == 0:
      return xs
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
  if( tdiff_samples == 0):
    return (data_x, data_y)
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





def discriminate(time,y,thresh,**kwargs):
    
  # argument structure has changed! no more hysteresis definiton by default
  
  # pk2pk hysteresis, difference between upper and lower threshold
  hysteresis = kwargs.get("hysteresis",0)               
  # if offset==0 -> hysteresis is symmetrical around thresh
  hyst_offset = kwargs.get("hyst_offset",0)
    
  interpolate = kwargs.get("interpolate",True)
  
  multi_hit = kwargs.get("multi_hit",False)
    
  out = np.zeros(len(y))
  
  rising_thresh  = thresh + hysteresis/2 + hyst_offset
  falling_thresh = thresh - hysteresis/2 + hyst_offset
    

  
  state = 1
  t1 = None
  tot = None

  t1_list = []
  tot_list = []
    
  for i in range(0,len(y)):
    v = y[i]
    
    if state == 1: 
      if v > rising_thresh:
        state = 0
        if t1 is None:
          if (interpolate and (i>0)):
            dt = time[i]-time[i-1]
            dy = y[i] - y[i-1]
            thresh_frac = (rising_thresh - y[i-1])/dy
            t1 = time[i-1] + dt*thresh_frac
          else:
            t1 = time[i]
    else: #state == 0
      if v < falling_thresh:
        state = 1
        if tot is None:
          if (interpolate and (i>0)):
            dt = time[i]-time[i-1]
            dy = y[i] - y[i-1] # negative
            thresh_frac = (falling_thresh - y[i-1])/dy
            tot = time[i-1] + dt*thresh_frac -t1
          else:
            tot = time[i] - t1
            
          if t1 is None:
            t1 = float('nan')
          if tot is None:
            tot = float('nan')
          t1_list += [t1]
          tot_list += [tot]
          if multi_hit:
            t1  = None
            tot = None
    
    out[i] = state
  if multi_hit:  
    return (1-out, np.array(t1_list), np.array(tot_list))
  else:
    t1 = float('nan')
    tot = float('nan')
    if len(t1_list):
      t1 = t1_list[0]
    if len(tot_list):
      tot = tot_list[0]
    return (1-out, t1, tot)





def rise_time(time,y,**kwargs):
  lo = kwargs.get("lo",0)
  hi = kwargs.get("hi",np.max(y))
  
  lo_thresh = kwargs.get("lo_thresh",hi*0.1)
  hi_thresh = kwargs.get("hi_thresh",hi*0.9)

  dummy, lo_time, dummy = discriminate(time,y,lo_thresh)
  dummy, hi_time, dummy = discriminate(time,y,hi_thresh)
  
  return (hi_time-lo_time)

def const_frac_discriminator(time,y,**kwargs):
  thresh = kwargs.get("thresh",0.2)
  # hysteresis kwargs argument is passed to discriminate function
  dummy, t1, tot = discriminate(time,normalize_max(y),thresh,**kwargs)
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


def rising_edge_detect(y):
  return np.array(y) * (1- np.array(shift_vector(y,1)))
  
