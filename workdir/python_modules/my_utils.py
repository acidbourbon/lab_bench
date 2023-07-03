import json
import os



def hist2d(x,y,**kwargs):
  from matplotlib import pyplot as plt
  from matplotlib import colors
    
  import numpy as np

  xedges = kwargs.get("xedges",np.linspace(np.min(x),np.max(x),100))
  yedges = kwargs.get("yedges",np.linspace(np.min(y),np.max(y),100))
  logz   = kwargs.get("logz",False)
  
  
  H, xedges, yedges = np.histogram2d( x, y, bins=(xedges, yedges))
  H = H.T  # Let each row list bins with common y range.
  X, Y = np.meshgrid(xedges, yedges)
  
  #cmap = plt.get_cmap('PiYG')
  #cmap = plt.get_cmap('rainbow')
  #cmap = plt.get_cmap('magma')
  #cmap = plt.get_cmap('plasma')
  #// https://matplotlib.org/3.3.1/tutorials/colors/colormaps.html
  cmap = plt.get_cmap('jet')
  
  
  if(logz):
    plt.pcolormesh(X, Y, H, cmap=cmap, norm=colors.LogNorm())
  else:
    plt.pcolormesh(X, Y, H, cmap=cmap)
  
  plt.xlabel(kwargs.get("xlabel",""))
  plt.ylabel(kwargs.get("ylabel",""))
  plt.title(kwargs.get("title","Histogram Title"))
  plt.show()




def big_figure():
  from matplotlib import pyplot as plt
  from IPython.display import set_matplotlib_formats
  set_matplotlib_formats('png')
  plt.rcParams["figure.figsize"] = (12,9)

def small_figure():
  from matplotlib import pyplot as plt 
  from IPython.display import set_matplotlib_formats
  set_matplotlib_formats('png')
  plt.rcParams["figure.figsize"] = (6,4)


def get_file_json(name):
  if os.path.isfile(name) :
    fh = open(name,"r")
    obj= json.load(fh)
    fh.close()
    return obj
  raise NameError("file {:s} does not exist".format(name))

def write_file_json(name,obj):
  fh = open(name,"w")
  json.dump(obj,fh,indent=2,sort_keys=True)
  fh.close()

#def timestamp():
#  import os
#  return os.popen("""date '+%Y-%m-%d_%H-%M-%S'""").read().replace("\n","")


def archive(**kwargs):
  label = kwargs.get("label","")
  import os
  if(not(os.path.isdir("./archive"))):
    os.mkdir("./archive")
  data_dir = make_data_dir()
  notebook = notebook_path()
  #workdir = os.path.dirname(notebook)
  notebook_basename = os.path.basename(notebook)
  notebook_name = notebook_basename.replace(".ipynb","")
  timestamp = os.popen("""date '+%Y-%m-%d_%H-%M-%S'""").read().replace("\n","")
  archive_dir = "./archive/"+ timestamp + "_" + notebook_name
    
  if (label != ""):
    archive_dir += ("_" + label)
    
  if(not(os.path.isdir(archive_dir))):
    os.mkdir(archive_dir)
    
  os.system("cp {:s} {:s}/".format(notebook,archive_dir))
  os.system("cp -R {:s} {:s}/".format(data_dir,archive_dir))
  print("archived to {:s}".format(archive_dir))



  
  

def notebook_path():
    from notebook import notebookapp
    import urllib
    import json
    import os
    import ipykernel
    """Returns the absolute path of the Notebook or None if it cannot be determined
    NOTE: works only when the security is token-based or there is also no password
    """
    connection_file = os.path.basename(ipykernel.get_connection_file())
    kernel_id = connection_file.split('-', 1)[1].split('.')[0]

    for srv in notebookapp.list_running_servers():
        try:
            if srv['token']=='' and not srv['password']:  # No token and no password, ahem...
                req = urllib.request.urlopen(srv['url']+'api/sessions')
            else:
                req = urllib.request.urlopen(srv['url']+'api/sessions?token='+srv['token'])
            sessions = json.load(req)
            for sess in sessions:
                if sess['kernel']['id'] == kernel_id:
                    return os.path.join(srv['notebook_dir'],sess['notebook']['path'])
        except:
            pass  # There may be stale entries in the runtime directory 
    return None

def make_data_dir():
  import os
  notebook = notebook_path()
  my_data_dir = notebook.replace(".ipynb","_data")
  if(not(os.path.isdir(my_data_dir))):
    os.mkdir(my_data_dir)
  return my_data_dir

def clear_data_dir():
  import os
  data_dir = make_data_dir()
  os.system("rm -rf {:s}/*".format(data_dir))


def dump_notebook_data():
  import dill
  notebook = notebook_path()
  dbfile = notebook.replace(".ipynb",".db")
  dill.dump_session(dbfile)
    
    
# do show(plt) instead of plt.show() to automatically save figure as svg
def show(plt,**kwargs):  
  import os
  ext = kwargs.get("ext",".svg")
  data_dir = make_data_dir()

  files = os.listdir(data_dir) # returns list
  names = [] 
  for file in files:
    if ext in file:
      names += [file.replace(ext,"")]
  names.sort()

  plot_counter = 0

  if (len(names) > 0):
    plot_counter = int(names[-1])+1

  plotfile = data_dir+"/{:03d}{:s}".format(plot_counter,ext) 
  print("saving to "+plotfile)
  picklefile = plotfile.replace(ext,".pickle")
  print("saving to "+picklefile)

  import pickle
  fig = plt.gcf()
  pickle.dump(fig,open(picklefile,'wb'))
    
  plt.savefig(plotfile)

  plt.show()
    
def save_animation_frame(plt):
  import os
  ext = ".png"
  data_dir = animation_cache()

  files = os.listdir(data_dir) # returns list
  names = [] 
  for file in files:
    if ext in file:
      names += [file.replace(ext,"")]
  names.sort()

  plot_counter = 0

  if (len(names) > 0):
    plot_counter = int(names[-1])+1

  plotfile = data_dir+"/{:03d}{:s}".format(plot_counter,ext) 
  print("saving to "+plotfile)
  plt.savefig(plotfile)

def make_gif():
  anim_dir = animation_cache()
  import os
  from IPython.display import Image
  os.system("cd "+anim_dir+"; convert *.png animation.gif")
  with open(anim_dir+'/animation.gif','rb') as f:
    display(Image(data=f.read(), format='png'))
  clear_animation_cache()
    
    
def animation_cache():
  import os
  notebook = notebook_path()
  my_anim_dir = notebook.replace(".ipynb","_anim")
  if(not(os.path.isdir(my_anim_dir))):
    os.mkdir(my_anim_dir)
  return my_anim_dir

def clear_animation_cache():
  import os
  anim_dir = animation_cache()
  os.system("rm -rf {:s}".format(anim_dir))    

def pickle_this(this,name):
  import pickle
  picklefile = make_data_dir()+"/{:s}.pickle".format(name)
  print("saving to "+picklefile)
  pickle.dump(this,open(picklefile,'wb'))
    
def unpickle(name):
  import pickle
  picklefile = "{:s}".format(name)
  print("loading from "+picklefile)
  return pickle.load(open(picklefile,"rb"))

def load_plot_pickle(file):
  from matplotlib import pyplot as plt
  import pickle
  pickle.load(open(file,"rb"))

def write_csv(filename,vector_list,**kwargs):
  delimiter = kwargs.get("delimiter",", ")
  cols = len(vector_list)
  print(cols)
  rows = len(vector_list[0])
  print(rows)
  formatstring = ("{:e}"+delimiter)*(cols-1)+ "{:e}" + "\n"
  with open(filename,"w") as f:
    for i in range(len(vector_list[0])):
      values = []
      for j in range(cols):
        values += [vector_list[j][i]]
      f.write(formatstring.format(*values))
    f.close()
