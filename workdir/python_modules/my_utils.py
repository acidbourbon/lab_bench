import json
import os



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


