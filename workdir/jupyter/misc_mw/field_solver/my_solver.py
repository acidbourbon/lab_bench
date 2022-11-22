import numpy as np
from matplotlib import pyplot as plt

import copy


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
    #X, Y = np.meshgrid(self.xedges, self.yedges)
    #self.X = X
    #self.Y = Y
  def pos_to_index(self,x,y):
    j = int( (x-self.x_min)/self.x_step )
    i = int( (y-self.y_min)/self.y_step )
    return (i,j)
    
class field:
  def __init__(self, grid, nd=1):
    self.grid = grid
    self.nd   = nd
    self.matrix = np.zeros([len(self.grid.y_edges),len(self.grid.x_edges),self.nd])
  def reset_matrix(self):
    self.matrix = np.zeros([len(self.grid.y_edges),len(self.grid.x_edges),self.nd])
    
class conductor:
  def __init__(self,x_min,x_max,y_min,y_max,color="blue"):
    self.x_min = x_min
    self.x_max = x_max
    self.y_min = y_min
    self.y_max = y_max
    self.color = color
    
    
    
class qcarrier:
  def __init__(self, charge, conductor, mass=1):
    self.charge = charge
    self.conductor = conductor
    self.mass = mass
    self.x = np.random.random()*(self.conductor.x_max-self.conductor.x_min)+ self.conductor.x_min
    self.y = np.random.random()*(self.conductor.y_max-self.conductor.y_min)+ self.conductor.y_min
    self.vx = 0
    self.vy = 0
    
#def plot_particles(p_list):
#    x = []
#    y = []
#    for p in p_list:
#        x += [p.x]
#        y += [p.y]
#    plt.scatter(x,y)
    
def plot_particles(p_list):
    charges = [-1,+1]
    
    for charge in charges:
        x = []
        y = []
        for p in p_list:
            if p.charge == charge:
                x += [p.x]
                y += [p.y]
        plt.scatter(x,y,label="q = {}".format(charge))
    plt.legend()
    
def q_density_from_charges(q_density,p_list):
    q_density.reset_matrix()
    for particle in p_list:
        
        i,j = q_density.grid.pos_to_index(particle.x,particle.y)
        q_density.matrix[i,j,0] += particle.charge
        
    
def e_field_from_q_density(e_field,q_density):
    grid = e_field.grid
    
    e_field.reset_matrix()
    
    for ei in range(len(grid.y_edges)):
        ey = grid.y_edges[ei]
        for ej in range(len(grid.x_edges)):
            ex = grid.x_edges[ej]
    
            for qi in range(len(grid.y_edges)):
                qy = grid.y_edges[qi]
                for qj in range(len(grid.x_edges)):
                    qx = grid.x_edges[qj]
                    
                    Q = q_density.matrix[qi,qj,0]
                    
                    # no charge here, no contribution to the field
                    if Q == 0:
                        continue
                        
                    # for the time being don't handle r^2 == 0
                    if (qi == ei) and (qj == ej):
                        continue
                        
                    
                    delta_x = qx-ex
                    delta_y = qy-ey
                    rr = delta_x*delta_x + delta_y*delta_y
                    r = np.sqrt(rr)
                    delta_E_x = -Q/rr * delta_x/r
                    delta_E_y = -Q/rr * delta_y/r
                    
                    e_field.matrix[ei,ej,0] += delta_E_x
                    e_field.matrix[ei,ej,1] += delta_E_y
                    
                    
def e_field_from_particles(e_field,particles):
    grid = e_field.grid
    
    x_step = grid.x_step
    y_step = grid.y_step
    #diag_step = np.sqrt(x_step*x_step + y_step*y_step)
    
    e_field.reset_matrix()
    
    smooth_factor = 1
    
    for ei in range(len(grid.y_edges)):
        ey = grid.y_edges[ei]
        for ej in range(len(grid.x_edges)):
            ex = grid.x_edges[ej]
            
            force_x = 0
            force_y = 0
            
            for particle in particles:
            
                delta_x = particle.x - ex
                delta_y = particle.y - ey
                
                if abs(delta_x) < smooth_factor*x_step:
                    delta_x = np.sign(delta_x) * smooth_factor*x_step
                if abs(delta_y) < smooth_factor*y_step:
                    delta_y = np.sign(delta_y) * smooth_factor*y_step
                
                rr = delta_x*delta_x + delta_y*delta_y
                #rr += 1e-2
                r = np.sqrt(rr)
                
                force   =  -particle.charge/rr
                force_x += force * delta_x/r
                force_y += force * delta_y/r
    
                    
            e_field.matrix[ei,ej,0] += force_x
            e_field.matrix[ei,ej,1] += force_y
                    
def move_particles(p_list,strength,friction,granularity=0.01,vmax=1):
    new_p_list = []
    for particle in p_list:
        
        force_x = 0
        force_y = 0
        
        for other_particle in p_list:
        
            if other_particle == particle:
                continue
        
            delta_x = other_particle.x - particle.x 
            delta_y = other_particle.y - particle.y
            rr = delta_x*delta_x + delta_y*delta_y
            r = np.sqrt(rr)
            #if r < granularity:
            #    r = granularity
            r += granularity
            
            force = -strength * other_particle.charge * particle.charge/(r*r)
            force_x += force * delta_x/r
            force_y += force * delta_y/r
            
        new_particle = copy.copy(particle)
        
        new_particle.x += new_particle.vx
        new_particle.y += new_particle.vy
        
        new_particle.vx += force_x - friction*new_particle.vx
        new_particle.vy += force_y - friction*new_particle.vy
        
        v = np.sqrt(new_particle.vx*new_particle.vx +new_particle.vy * new_particle.vy)
        
        if v > vmax:
            new_particle.vx = new_particle.vx/v * vmax
            new_particle.vy = new_particle.vy/v * vmax
        
        
        if new_particle.x > new_particle.conductor.x_max:
            new_particle.x = new_particle.conductor.x_max
            new_particle.vx = 0
        elif new_particle.x < new_particle.conductor.x_min:
            new_particle.x = new_particle.conductor.x_min
            new_particle.vx = 0
            
        if new_particle.y > new_particle.conductor.y_max:
            new_particle.y = new_particle.conductor.y_max
            new_particle.vy = 0
        elif new_particle.y < new_particle.conductor.y_min:
            new_particle.y = new_particle.conductor.y_min
            new_particle.vy = 0
            
        new_p_list += [new_particle]
    return new_p_list