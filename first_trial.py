#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 17 15:14:50 2017

@author: ycanerol


Network simulator in python

Based off of Beggs Plenz 2003 and Beggs Haldemann 2005 papers


"""

import numpy as np
import matplotlib.pyplot as plt
from random import shuffle

# Initialization
# Enter and change parameters here

node_nr=100 # Should be a square for plotting
connections=4   # Defined as C in the paper
sigma=1

# For time iterations
time_steps=500 # How many times we transmit
spont_prob=0.001 # Proabability of  spontaneous activation of connections

plot_and_save=False # Should we plot and save the activation patterns? 
                    # Won't be neccesary for generating data for log-log plots
                    
number_of_simulations=200   # Make sure plot_and_save is False if you're running many simulations.                    
                    
log_plot_base=10    # Changes the base of the log-log plots on both axes
                    # Any base should give the same results       

#%% Functions
def set_array(node_nr):     # Function to set an array of empty arrays
    a=[[]for a in range(node_nr)]
    return a

def get_avalanches(array):  # Returns sizes of avalanches. Can be modified for time intervals for plotting
    times=[]
    avalanche_sizes=[]
    time_ranges=[]
    
    for i in range(len(array)): # Get activation as an array without duplicates
        if i==0: 
            times.append(array[i][0])  
        elif array[i][0]!=array[i-1][0]:
            times.append(array[i][0])
   
    # Get the time ranges for avalanches
    # Time ranges can later be used for plotting too.        
    first = last = times[0]
    for n in times[1:]:
        if n - 1 == last: # Part of the group, bump the end
            last = n
        else: # Not part of the group, append current group and start a new one
            time_ranges.append([first, last])
            first = last = n
    time_ranges.append([first, last]) # Append the last group
    
    #Calculate avalanche sizes from time ranges
    for i in time_ranges:
        avalanche_sizes.append(i[1]-i[0]+1)

    return avalanche_sizes        


#%% Running many simulations    
all_avalanche_sizes=[]

for i in range(number_of_simulations): 
    #%% Generating the network
    nodes=set_array(node_nr)
    # Nodes list will contain lists indices of connected nodes to each element
    
    for i in range(node_nr):
        a=list(range(node_nr))
        shuffle(a)
        # We shuffle the index list, the connections of current node will be taken from here
        
        nodes[i]=a[:connections+1]
        # We take one more than needed, in case one of the indices point to the neuron itself
        
        flag=True
        for j in range(connections):
            if nodes[i][j]==i:
                flag=False
                nodes[i].remove(i)
                # Remove self-connection
        if flag:
            del nodes[i][-1]
            # If we removed no self-connections, delete the extra index at the end.
    
    #%% Setting up transmission probabilities        
    # We established a recurrent network, we need to establish transmission proabability for each connection
    flag=True
    prob_iteration_count=0
    while flag:
        tr_probabilities=set_array(node_nr)
        for i in range(node_nr):
            divider=list(np.sort(np.random.random_sample(connections-1)))
            divider.insert(0,0)
            divider.append(1)
            divider=list(np.multiply(divider,sigma)) # Scale the interval to be the size of sigma
            for k in range(1,len(divider)):
                tr_probabilities[i].append(divider[k]-divider[k-1])
                # The constraint is that for each node sigma_i should be equal to sigma
                # Sums of the probabilities for one node should be sigma
                # For this, we divide the sigma into C parts and use the sizes of the parts as probabilities
        all_less_than1=True
        for i in range(node_nr):
            for k in range(connections):
                if tr_probabilities[i][k]>1:
                    all_less_than1=False
        if all_less_than1:
            flag=False
        if prob_iteration_count>10000: # Deals with the case that C and sigma are inappropriate, prevents infinite loop
            raise ValueError('More than 10.000 iterations when setting up probabilities, terminating. There are >1 probabilities.')
            break
        prob_iteration_count+=1
    del j,k,a,divider,flag
    # The network is set up with required properties at this point
    
    #%% Incorporating time and inputs
    
    outputs=list(np.zeros(node_nr)) # Holds the state of each node.
    activated=[]
    
    for t in range(time_steps):
        
        inputs=outputs # The outputs of the previous iteration are inputs of current.
        outputs=list(np.zeros(node_nr)) 
        
        for i in range(node_nr):
            for k in range(connections):
                if np.random.random()<spont_prob:              
                    outputs[nodes[i][k]]=1
                elif inputs[i] and np.random.random()<tr_probabilities[i][k]:
                    outputs[nodes[i][k]]=1  # No else statement so if the same node was activated 
                                            # by another connection, it will not be changed.
            if outputs[i]:
                activated.append([t,i])   
                
        #%% Plotting individual frames
        
        # Plot individial frames & save img for each round
        if plot_and_save:
            node_nr_sqrt=int(np.sqrt(node_nr))  # Get size of one side of the square to plot
            img = plt.matshow(np.reshape(outputs,[node_nr_sqrt,node_nr_sqrt]), cmap="Greys")
            # Convert to a square matrix and plot      
            
            images_savedir='/Users/ycan/Documents/projects/network-sim-pics/'
            
            plt.savefig(images_savedir+"{0:0>3}".format(str(t))+'.jpg')
            plt.close()
        
        # Use ImageJ to generate .avi file from the images.
        # Also possible with cv2 or matplotlib but requires more work.
    
                    
 
#%% Gathering avalanches
    
        
    avalanche_sizes=get_avalanches(activated)    
    all_avalanche_sizes=all_avalanche_sizes+avalanche_sizes
    
print("{:<5} simulations ran, {:<5} data points were generated.".format(number_of_simulations,len(all_avalanche_sizes)))    

#%% Generating lol-log plot, Avalanche lengths histogram

log_max=np.log(max(all_avalanche_sizes))/np.log(log_plot_base)
# Define the upper border for x axis bins                
plt.hist(all_avalanche_sizes,bins=np.logspace(0,log_max,base=log_plot_base))
plt.xscale('log',basex=log_plot_base)
plt.yscale('log',basey=log_plot_base)
plt.show()


