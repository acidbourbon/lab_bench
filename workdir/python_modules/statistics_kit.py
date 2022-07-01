import random
import numpy as np

def uniformize(x,y,**kwargs):
  out_x_list = []
  out_y_list = []
    
  xedges=kwargs.get("xedges",np.linspace(np.min(x),np.max(x),20))
  target_entries = kwargs.get("target_entries",100)
    

  for i in range(0,len(xedges)-1):
    l = xedges[i]
    r = xedges[i+1]
    mask = (x>=l)&(x<r)
    sel_x = x[mask]
    sel_y = y[mask]
    entries = len(sel_x)
    if(entries > 0):
      for j in range(0,target_entries):
        k = random.randint(0,entries-1)
        out_x_list += [sel_x[k]]
        out_y_list += [sel_y[k]]
    
    #print("bin {:d}: {:d} entries".format(i,entries))
  return (np.array(out_x_list), np.array(out_y_list)) 

def median_slices(x,y,**kwargs):
  out_x_list = []
  out_y_list = []
    
  n_bins = kwargs.get("n_bins",20)
    
  xedges=kwargs.get("xedges",np.linspace(np.min(x),np.max(x),n_bins))
    

  for i in range(0,len(xedges)-1):
    l = xedges[i]
    r = xedges[i+1]
    mask = (x>=l)&(x<r)
    sel_x = x[mask]
    sel_y = y[mask]
    entries = len(sel_x)
    if(entries > 0):
      out_x_list += [np.median(sel_x)]
      out_y_list += [np.median(sel_y)]
    
  return (np.array(out_x_list), np.array(out_y_list)) 

def median_x_std_y_slices(x,y,**kwargs):
  out_x_list = []
  out_y_list = []
  
  n_bins = kwargs.get("n_bins",20)
    
  xedges=kwargs.get("xedges",np.linspace(np.min(x),np.max(x),n_bins))
    

  for i in range(0,len(xedges)-1):
    l = xedges[i]
    r = xedges[i+1]
    mask = (x>=l)&(x<r)
    sel_x = x[mask]
    sel_y = y[mask]
    entries = len(sel_x)
    if(entries > 0):
      out_x_list += [np.median(sel_x)]
      out_y_list += [np.std(sel_y)]
    
  return (np.array(out_x_list), np.array(out_y_list)) 



def med3_filter(data):
  out = []
  len_data = len(data)
  out += [data[0]]
  for i in range(1,len_data-1):
    med = np.median([data[i-1:i+2]])
    if ~(np.isnan(med)):
      out += [med]
    else:
      out += [data[i]]
  out += [data[len_data-1]]
  return np.array(out)

def pearson(x,y):
  x_ = np.array(x)
  y_ = np.array(y)
  my_sum = 0
  mean_x = np.mean(x_)
  mean_y = np.mean(y_)
  for i in range(0,len(x_)):
    my_sum += (x_[i]-mean_x)*(y_[i]-mean_y)
  return (my_sum/(len(x_)))/(np.std(x_)*np.std(y_))


def pearson_regression(x,y):
  x_ = np.array(x)
  y_ = np.array(y)
  my_sum = 0
  mean_x = np.mean(x_)
  mean_y = np.mean(y_)
  for i in range(0,len(x_)):
    my_sum += (x_[i]-mean_x)*(y_[i]-mean_y)
  r = (my_sum/(len(x_)))/(np.std(x_)*np.std(y_))
  m = r * np.std(y_)/np.std(x_)
  y0 = mean_y- m * mean_x
  return m,y0
