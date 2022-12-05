import numpy as np
from matplotlib import pyplot as plt

import copy
from numpy.fft import fft2, ifft2


eps_0 = 8.854187817e-12
mu_0  = 1.256637061e-6

def coarsen_grid(g,n=1):
    # create an identical grid to g, but with pixels twice as big
    small_grid = grid(g.x_min,g.x_max,g.x_step*(2**n),g.y_min,g.y_max,g.y_step*(2**n))
    
    return small_grid


def up4scale(M):
    m,n = M.shape
    N = np.zeros([m*2,n*2])
    N[0::2,0::2] = M
    N[1::2,0::2] = M
    N[0::2,1::2] = M
    N[1::2,1::2] = M
    
    # next neighbor interpolation
    N[1:-2:2,0::2]   = 0.5*(N[0:-3:2,0::2] + N[2:-1:2,0::2])
    N[0::2,1:-2:2,]  = 0.5*(N[0::2,0:-3:2] + N[0::2,2:-1:2])
    N[1:-2:2,1:-2:2] = 0.5*(N[0:-3:2,0:-3:2] + N[2:-1:2,2:-1:2])
    
    #N[1:-3:2,0::2]   = 0.5*(M[0:-2,0:]   + M[1:-1,0:])
    #N[0::2,1:-3:2]  = 0.5*(M[0:,0:-2]   + M[0:,1:-1])
    #N[1:-3:2,1:-3:2] = 0.5*(M[0:-2,0:-2] + M[1:-1,1:-1])
    
    return N

#def coarse_matrix(M,n=1):
#    return M[::(2**n),::(2**n)]

def coarsen_field(F,n=1):
    new_grid = coarsen_grid(F.grid,n=n)
     
    new_field = field(new_grid, nd=F.nd)
    if F.nd == 1:
        new_field.matrix = F.matrix[::(2**n),::(2**n)]
    else:
        new_field.matrix = F.matrix[::(2**n),::(2**n),:]
    return new_field
        
                                               
    

class grid:
    def __init__(self,x_min,x_max,x_step,y_min,y_max,y_step):
        self.x_min   = x_min
        self.x_max   = x_max
        self.x_step  = x_step
        self.y_min   = y_min
        self.y_max   = y_max
        self.y_step  = y_step
        self.area_element = x_step * y_step
        self.x_edges = np.arange(x_min,x_max,x_step)
        self.y_edges = np.arange(y_min,y_max,y_step)
        self.X, self.Y = np.meshgrid(self.x_edges, self.y_edges)
        self.shape = (len(self.y_edges),len(self.x_edges))
        
    def pos_to_index(self,x,y):
        j = int( (x-self.x_min)/self.x_step )
        i = int( (y-self.y_min)/self.y_step )
        max_i = len(self.y_edges)-1
        max_j = len(self.x_edges)-1
        
        i = np.min([i,max_i])
        i = np.max([i,0])
        j = np.min([j,max_j])
        j = np.max([j,0])
        
        return (i,j)
    
    def B_kernel(self):
    
        x_step = self.x_step
        y_step = self.y_step
        area_element = x_step * y_step
    
        lenj = 2*len(self.x_edges)
        leni = 2*len(self.y_edges)
        
        B = np.zeros([leni,lenj,2])
        
        ii = int(leni/2)
        jj = int(lenj/2)
        
        for i in range(leni):
            for j in range(lenj):
                
                dy = y_step*(ii-i)    
                dx = x_step*(jj-j)
                dpow2  = dx**2+dy**2 # d**2
                
                if dpow2 == 0:
                    continue
                
                B[i,j,0] += 1./dpow2 * (-dy)
                B[i,j,1] += 1./dpow2 * ( dx)
        B *= mu_0/(2*np.pi)
        return B
    

def Bconv(j,k):
    # this folds the B field from a thin wire (k)
    # with the current density (j)
    # k is twice the size of j
    
    si,sj = j.shape
    jj = np.zeros([si*2,sj*2])
    #kk = np.zeros([si*2,sj*2])
    
    jj[0:si,0:sj] = j
    #kk[0:si,0:sj] = k
    kk = k
    
    fr  = fft2(jj)
    fr2 = fft2(np.flipud(np.fliplr(kk)))
    cc = np.real(ifft2(fr*fr2))
    cc = np.roll(cc, int(-si+1),axis=0)
    cc = np.roll(cc, int(-sj+1),axis=1)
    
    return cc[0:si,0:sj]
    
def B_from_J(J,conductor_mask=None): # J is the current density
    B_kernel = J.grid.B_kernel()
    B = field(J.grid,nd=2)
    
    if(conductor_mask is None):
        B.matrix[:,:,0] = Bconv(J.matrix,B_kernel[:,:,0])
        B.matrix[:,:,1] = Bconv(J.matrix,B_kernel[:,:,1])
    else:
        mask = 1-conductor_mask.matrix
        B.matrix[:,:,0] = Bconv(J.matrix,B_kernel[:,:,0])*mask
        B.matrix[:,:,1] = Bconv(J.matrix,B_kernel[:,:,1])*mask
    return B

def B_of_conductors(J,conductor_list):
    
    Jmasked = field(J.grid)
    conductor_mask, dummy = conductors_to_mask(J.grid,conductor_list)
    Jmasked.matrix = J.matrix * conductor_mask.matrix
   
    return B_from_J(Jmasked,conductor_mask)
    
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
    def abs_matrix(self):
        if self.nd > 1:
            m = np.zeros([len(self.grid.y_edges),len(self.grid.x_edges)])
            for d in range(self.matrix.shape[2]):
                m += self.matrix[:,:,d]**2
            return np.sqrt(m)
        else:
            return np.abs(self.matrix)
    
class conductor:
  def __init__(self,x_min,x_max,y_min,y_max,color="blue",V=0):
    self.x_min = x_min
    self.x_max = x_max
    self.y_min = y_min
    self.y_max = y_max
    self.V = V 
    self.color = color
    
    self.x_center = (x_max + x_min)/2.
    self.y_center = (y_max + y_min)/2.
    
class dielectric:
  def __init__(self,x_min,x_max,y_min,y_max,color="green",eps_r=1):
    self.x_min = x_min
    self.x_max = x_max
    self.y_min = y_min
    self.y_max = y_max
    self.eps_r = eps_r 
    self.color = color
    self.x_center = (x_max + x_min)/2
    self.y_center = (y_max + y_min)/2
    
    
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

def D_from_V(potential,epsilon):
    
    D = E_from_V(potential)
    D.matrix[:,:,0] *= epsilon.matrix
    D.matrix[:,:,1] *= epsilon.matrix
    
    return D
    
def rho_from_V(potential,epsilon=eps_0):
    
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
    
    my_epsilon = epsilon
    if type(epsilon) == field:
        my_epsilon = epsilon.matrix

    rho.matrix = -my_epsilon*( (neigh_U + neigh_D - 2*potential.matrix) / (y_step*y_step) \
                         +(neigh_L + neigh_R - 2*potential.matrix) / (x_step*x_step) )
    
    return rho

def relax_2D_dielectric(potential,fixed_mask,epsilon):
    old_matrix = potential.matrix
    eps_matrix = np.sqrt(epsilon.matrix)

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
    
    eps_R = eps_matrix.copy()
    eps_L = eps_matrix.copy()
    eps_U = eps_matrix.copy()
    eps_D = eps_matrix.copy()
    eps_D[1:-1,:] = eps_matrix[0:-2,:]
    eps_U[0:-2,:] = eps_matrix[1:-1,:]
    eps_R[:,0:-2] = eps_matrix[:,1:-1]
    eps_L[:,1:-1] = eps_matrix[:,0:-2]
    

    potential.matrix[:,:] =  1./(eps_R + eps_L + eps_U + eps_D) \
       *(  eps_L * neigh_L \
         + eps_R * neigh_R \
         + eps_U * neigh_U \
         + eps_D * neigh_D )*omask\
       + old_matrix*fmask
    
def gen_dielectric_field(grid,dielectric_list):
    epsilon = field(grid)
    epsilon.matrix += eps_0
    
    for dielectric in dielectric_list:
        i_min, j_min = grid.pos_to_index(dielectric.x_min,dielectric.y_min)
        i_max, j_max = grid.pos_to_index(dielectric.x_max,dielectric.y_max)
        size_i = i_max - i_min 
        size_j = j_max - j_min 
        epsilon.matrix[i_min:i_max,j_min:j_max] = np.ones([size_i,size_j])*dielectric.eps_r*eps_0
        
    return epsilon

def charge_on_conductor(rho,conductor):
    c_mask, dummy = conductors_to_mask(rho.grid,[conductor])
    area_element = rho.grid.x_step * rho.grid.y_step
    return np.sum(rho.matrix * c_mask.matrix) * area_element


def conductor_link(grid,conductor1,conductor2):
    link = field(grid)
    
    i1,j1 = grid.pos_to_index(conductor1.x_center,conductor1.y_center)
    link.matrix[i1,j1] = 1
    i2,j2 = grid.pos_to_index(conductor2.x_center,conductor2.y_center)
    link.matrix[i2,j2] = 1
    
    di = i2-i1
    dj = j2-j1
    
    dy = di * grid.y_step
    dx = dj * grid.x_step
    
    npix = np.max([abs(di),abs(dj)])
    
    for k in range(npix):
        ii = i1 + round(di*k/npix)
        jj = j1 + round(dj*k/npix)
        link.matrix[ii,jj] = 1
        
    npix += 1  # number of pixels that have been drawn
    
    length = np.sqrt((dj*grid.x_step)**2 + (di*grid.y_step)**2)
    
    normal_vec = np.array([-dy,dx])/np.sqrt(dx**2+dy**2)
    
    dl = length/(npix-1)
    
    return link , dl, normal_vec


def B_of_conductors(J,conductor_list):
    
    Jmasked = field(J.grid)
    conductor_mask, dummy = conductors_to_mask(J.grid,conductor_list)
    Jmasked.matrix = J.matrix * conductor_mask.matrix
   
    return B_from_J(Jmasked,conductor_mask)


def flux_between_conductors(B,conductor1,conductor2):
    
    link , dl, normal_vec = conductor_link(B.grid,conductor1,conductor2)
    
    phi   = dl*( np.sum(link.matrix * B.matrix[:,:,0] * normal_vec[0])
                +np.sum(link.matrix * B.matrix[:,:,1] * normal_vec[1]) )
    return phi
    

def poynting_z(E,B):
    Sz = field(E.grid)

    # poynting vector = ExB
    
    Ex = E.matrix[:,:,0] 
    Ey = E.matrix[:,:,1] 
    Bx = B.matrix[:,:,0] 
    By = B.matrix[:,:,1] 
    
    Sz.matrix = (Ex*By - Ey*Bx)/mu_0
    return Sz


##################################################
##                  graveyard                   ##
##################################################


# calculate B field without convolution

#def B_of_conductor(conductor,rho,fixed_mask):
#
#    my_grid = rho.grid
#
#    B = field(my_grid,nd=2)
#
#    conductor_mask, dummy = conductors_to_mask(my_grid,[conductor])
#
#    I = rho.matrix * conductor_mask.matrix
#    signI = np.sign(I)
#    I *= signI/np.sum(I)
#
#
#    inmask = conductor_mask.matrix
#    outmask = 1-fixed_mask.matrix
#
#    x_step = my_grid.x_step
#    y_step = my_grid.y_step
#
#
#    leni, lenj = I.shape
#
#    for i in range(leni):
#        for j in range(lenj):
#
#            if not(outmask[i,j]):
#                continue
#
#            for ii in range(leni):
#                for jj in range(lenj):
#
#                    if not(inmask[ii,jj]):
#                        continue
#                    dy = y_step*(ii-i)    
#                    dx = x_step*(jj-j)
#                    d  = np.sqrt(dx**2+dy**2)
#                    B.matrix[i,j,0] += 1./d**3 * I[ii,jj] * (-dy)
#                    B.matrix[i,j,1] += 1./d**3 * I[ii,jj] * ( dx)
#    B.matrix *= mu_0/(2*np.pi)
#    return B
                
        
