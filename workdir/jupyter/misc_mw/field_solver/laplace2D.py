import numpy as np
from matplotlib import pyplot as plt

import copy


eps_0 = 8.854187817e-12

class grid:
  def __init__(self,x_min,x_max,x_step,y_min,y_max,y_step):
    self.x_min   = x_min
    self.x_max   = x_max
    self.x_step = x_step
    self.y_min   = y_min
    self.y_max   = y_max
    self.y_step = y_step
    self.x_edges = np.arange(x_min,x_max,x_step)
    self.y_edges = np.arange(y_min,y_max,y_step)
    self.X, self.Y = np.meshgrid(self.x_edges, self.y_edges)
  def pos_to_index(self,x,y):
    j = int( (x-self.x_min)/self.x_step )
    i = int( (y-self.y_min)/self.y_step )
    return (i,j)
    
class field:
  def __init__(self, grid, nd=1):
    self.grid = grid
    self.nd   = nd
    if self.nd > 1:
        self.matrix = np.zeros([len(self.grid.y_edges),len(self.grid.x_edges),self.nd])
    else:
        self.matrix = np.zeros([len(self.grid.y_edges),len(self.grid.x_edges)])
  def reset_matrix(self):
    if self.nd > 1:
        self.matrix = np.zeros([len(self.grid.y_edges),len(self.grid.x_edges),self.nd])
    else:
        self.matrix = np.zeros([len(self.grid.y_edges),len(self.grid.x_edges)])
    
class conductor:
  def __init__(self,x_min,x_max,y_min,y_max,color="blue",V=0):
    self.x_min = x_min
    self.x_max = x_max
    self.y_min = y_min
    self.y_max = y_max
    self.V = V 
    self.color = color
    
class dielectric:
  def __init__(self,x_min,x_max,y_min,y_max,color="green",eps_r=1):
    self.x_min = x_min
    self.x_max = x_max
    self.y_min = y_min
    self.y_max = y_max
    self.eps_r = eps_r 
    self.color = color
    
    
def conductors_to_mask(grid,conductor_list):
    fixed_mask      = field(grid)
    start_potential = field(grid)
    
    for conductor in conductor_list:
        i_min, j_min = grid.pos_to_index(conductor.x_min,conductor.y_min)
        i_max, j_max = grid.pos_to_index(conductor.x_max,conductor.y_max)
        size_i = i_max - i_min 
        size_j = j_max - j_min 
        fixed_mask.matrix[i_min:i_max,j_min:j_max]      = np.ones([size_i,size_j])
        start_potential.matrix[i_min:i_max,j_min:j_max] = np.ones([size_i,size_j])*conductor.V
        
    return fixed_mask, start_potential
        
def relax_2D(potential,fixed_mask):
    old_matrix = potential.matrix

    # fixed potential areas
    fmask = fixed_mask.matrix
    # open areas - free space where the field spreads
    omask = 1 - fmask

    neigh_R = old_matrix.copy()
    neigh_R[:,0:-2] = old_matrix[:,1:-1]
    neigh_L = old_matrix.copy()
    neigh_L[:,1:-1] = old_matrix[:,0:-2]
    neigh_U = old_matrix.copy()
    neigh_U[0:-2,:] = old_matrix[1:-1,:]
    neigh_D = old_matrix.copy()
    neigh_D[1:-1,:] = old_matrix[0:-2,:]

    potential.matrix[:,:] = 0.25*(neigh_U + neigh_D + neigh_L + neigh_R)*omask + old_matrix*fmask
    
def E_from_V(potential):
    
    E      = field(potential.grid,nd=2)
    x_step = potential.grid.x_step
    y_step = potential.grid.y_step
    
    Ex = copy.copy(potential.matrix)
    Ey = copy.copy(potential.matrix)
    
    Ex[:,0:-2] = -(Ex[:,1:-1] - Ex[:,0:-2])/x_step
    Ey[0:-2,:] = -(Ey[1:-1,:] - Ey[0:-2,:])/y_step
    
    E.matrix[:,:,0] = Ex
    E.matrix[:,:,1] = Ey
    
    return E
    
def rho_from_V(potential):
    
    rho    = field(potential.grid)
    x_step = potential.grid.x_step
    y_step = potential.grid.y_step
    

    neigh_R = potential.matrix.copy()
    neigh_R[:,0:-2] = potential.matrix[:,1:-1]
    neigh_L = potential.matrix.copy()
    neigh_L[:,1:-1] = potential.matrix[:,0:-2]
    neigh_U = potential.matrix.copy()
    neigh_U[0:-2,:] = potential.matrix[1:-1,:]
    neigh_D = potential.matrix.copy()
    neigh_D[1:-1,:] = potential.matrix[0:-2,:]

    rho.matrix = -eps_0*( (neigh_U + neigh_D - 2*potential.matrix) / (y_step*y_step) \
                         +(neigh_L + neigh_R - 2*potential.matrix) / (x_step*x_step) )
    
    return rho
