import numpy as np
from matplotlib import pyplot as plt
import pandas as pd

from my_utils import *

prop_cycle = plt.rcParams['axes.prop_cycle']
colors = prop_cycle.by_key()['color']



def pop_count(string):
    return len("{:0128b}".format(int(string,16)).replace("0",""))


def fast_hist(values,start,stop,bin_width):
    x = np.arange(start,stop,bin_width)
    y = x*0
    last_bin = len(x)-1
    for val in values:
        pos = int( np.floor( (val-start)/bin_width ))
        if ( (pos >= 0) and (pos <= last_bin) ):
            y[pos]+=1
    return (x,y)

def calc_IQ(istart,qstart,iqlen,tdl):
    
    Iraw = [ x[istart:istart+iqlen] for x in tdl ]
    Qraw = [ x[qstart:qstart+iqlen] for x in tdl ]

    I = np.array(list(map(pop_count, Iraw))) - int(iqlen/2)
    Q = np.array(list(map(pop_count, Qraw))) - int(iqlen/2)
    
    return (I,Q)

# Function to format ticks as multiples of π
def format_ticks(val, pos):
    if val == 0:
        return '0'
    elif val == 0.5:
        return 'π/2'
    elif val == -0.5:
        return '-π/2'
    elif val == 1:
        return 'π'
    elif val == -1:
        return '-π'
    elif val == 2 * np.pi:
        return '2π'
    elif val == -2 * np.pi:
        return '-2π'
    else:
        return f'{val/np.pi:.0f}π'






def ana_rot(I,Q,itime,**kwargs):
    
    
    plot = kwargs.get("plot",False)
    
    
    colors = prop_cycle.by_key()['color']
    colors = colors * 16

    if (plot): 
        plt.rcParams["figure.figsize"] = (5,4)

        #big_figure()

        fig, ax = plt.subplots()
        # Set major ticks at multiples of π/2
        #ax.xaxis.set_major_locator(MultipleLocator(base=0.5))
        # Apply the formatting function
        #ax.xaxis.set_major_formatter(FuncFormatter(format_ticks))
        ax.grid(True)

    
    phi = np.arctan2(Q,I)
    
    rotations   = np.array([])
    gap_centers = np.array([])


    
    last_gap_center = 0
    rotation = 0
    
    my_range = int(np.max(itime))+1
    
    last_start_of_block = -1000
    last_end_of_block   = -1000
    last_block_center   = -1000
    last_block_over_gap      = False
    

    for i in range(my_range):
        mask = (itime == i)
        phiset=phi[mask]
        
        
            
        gap_center = 0
            
        if len(phiset) > 0:
        
            phiset.sort()
            
            rot_phiset = np.concatenate((phiset[1:],phiset[:1])) 
            
            distance = (rot_phiset - phiset) % (2*np.pi)
            
            end_of_block = phiset[np.argmax(distance)]
            start_of_block = phiset[ (np.argmax(distance)+1) % len(phiset) ]
            max_distance  = np.max(distance)
            block_width   = 2*np.pi - max_distance
            gap_center = ((end_of_block + max_distance/2 + np.pi) % (2*np.pi)) - np.pi
            block_center = ((start_of_block + block_width/2 + np.pi) % (2*np.pi)) - np.pi
            #plt.plot(distance)
            #plt.show()
            if(0):
                print("gap distance: {}".format(max_distance))
                print("start of block: {}".format(start_of_block))
                print("end of block: {}".format(end_of_block))
                print("gap center: {}".format(gap_center))
                print("block center: {}".format(block_center))
            
            block_over_gap = block_center > gap_center
            
            #if (last_block_over_gap == False) and (block_over_gap == True):
                #rotation += 1
            if gap_center < last_gap_center:
                rotation += 1
                
            #print("counted rotations: {}".format(rotation))
            
            last_gap_center     = gap_center
            last_start_of_block = start_of_block
            last_end_of_block   = end_of_block
            last_block_center   = block_center
            last_block_over_gap = block_over_gap
            
            if(plot):
                #print("i = {}".format(i))

                #ax.hist(phiset/np.pi,bins=np.arange(-1,1,.025))

                ax.scatter( 
                    phiset/np.pi,
                    np.zeros(len(phiset)) + i + 0.25*(np.random.random(len(phiset))-0.5),
                    s=6,
                    c=colors[i]
                )

                marker_size=150
                ax.scatter( 
                    [gap_center/np.pi],
                    [i],
                    s=marker_size,
                    c=colors[i],
                    marker="x"
                )

                marker_size=300
                ax.scatter( 
                    [start_of_block/np.pi],
                    [i],
                    s=marker_size,
                    c=colors[i],
                    marker="|"
                )
                ax.scatter( 
                    [end_of_block/np.pi],
                    [i],
                    s=marker_size,
                    c=colors[i],
                    marker="|"
                )


                #ax.set_yticks(list(range(5)))

                ax.set_xticks([-1,-0.5,0,0.5,1])

                #plt.show()
            
        gap_centers = np.append(gap_centers,[gap_center])
        rotations   = np.append(rotations,[rotation])
        
        
    
    if(plot):
        #plt.savefig("gap_centers.svg")
        plt.xlabel("phi")
        plt.ylabel("itime")
        plt.show()
        
    #print(gap_centers)
   
    if(plot):
        idx = list(range(my_range))
        plt.plot(idx,rotations)
        plt.scatter(idx,rotations,label="rotations")
        plt.plot(idx,gap_centers)
        plt.scatter(idx,gap_centers,label="gap centers")
        plt.title("unfolding analysis")
        plt.legend()
        plt.xlabel("intermediate time")
        plt.show()
        
    return (rotations,gap_centers)

def cont_phi_new(I,Q,itime,rotations,gap_centers):
    
    phi = np.arctan2(Q,I)
    
    new_phi = np.zeros(len(phi))
    
    for i, phival in enumerate(phi):
        
        index = int(itime[i]) 
        if phival >= gap_centers[index]: # the lower valued part
                new_phi[i] = phival  + (rotations[index])*2*np.pi
        else: # higher valued part
                new_phi[i] = phival  + (rotations[index]+1)*2*np.pi
        
        
        
    return new_phi + np.pi


def calib_ftime(cphi,calib_curve,phistep,period):
    ftime = np.zeros(len(cphi))
    
    for i, phival in enumerate(cphi):
        ftime[i] = period * calib_curve[int(phival/phistep)]
        
    return ftime
    