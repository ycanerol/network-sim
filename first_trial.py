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
from datetime import datetime

#%%
# Initialization
# Enter and change parameters here

node_nr=64 # Should be a square for plotting
connections=4   # Defined as C in the paper
sigma=1

# For time iterations
time_steps=200 # How many times we transmit
spont_prob=0.001 # Proabability of  spontaneous activation of connections

single_input_mode=True # No spontaneous activity, give a single input, observe the avalanches

plot_and_save=False # Should we plot and save the activation patterns? 
                    # Won't be neccesary for generating data for log-log plots
images_savedir='/Users/ycan/Documents/projects/network-sim-pics/'

                    
number_of_simulations=20000   # Make sure plot_and_save is False if you're running many simulations.                    
                    
log_plot_base=10    # Changes the base of the log-log plots on both axes
                    # Any base should give the same results
                    
uniform_tr_prob=True # In the paper, they have used 1/sigma for all transmission probabilities
                      # trying with the same method. Our normal method generates a lot of variation                

#%% Functions and setup

if single_input_mode:
    spont_prob=0

def set_array(node_nr):     # Function to set an array of empty arrays
    a=[[]for a in range(node_nr)]
    return a

def get_avalanches(array):  # Returns sizes and length (in number of frames) of avalanches
                            # Avalanche size is defined as number of activated nodes in one avalanche
    times=[]
    avalanche_sizes=[0] # Initialize the first avalanche size as 0, the first iteration will add 1
    avalanche_frame_lengths=[]
    time_ranges=[]
    
    for i in range(len(array)): # Get activation as an array without duplicates
        if i==0: 
            times.append(array[i][0])  
        elif array[i][0]!=array[i-1][0]:
            times.append(array[i][0])
        
        if array[i][0]-array[i-1][0]<=1: # If we are stil in an avalanche, add 1 for each activated node for avalanche sizes
            avalanche_sizes[-1]+=1
        else:
            avalanche_sizes.append(1) # If we exit an avalanche, start counting the size of the next one
   
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
        avalanche_frame_lengths.append(i[1]-i[0]+1)

    return avalanche_frame_lengths,avalanche_sizes        


#%% Running many simulations    
all_avalanche_sizes=[]
all_avalanche_frame_lengths=[]

execution_timer=datetime.now() # To see how long simulations or plotting takes

if plot_and_save and number_of_simulations>1: # Many write cycles is undesirable, catch if this happens
    print('Plot and save is active and many simulations will be run.')
    print('This will write many times on your disk with no result.')
    print('Please turn off plotting for simulations.')

    input('\nPress ENTER to continue with one round of simulation or CTRL+C to stop the script.\n')
    number_of_simulations=1
    
    print('Plotting.')
    
#%%
for i in range(number_of_simulations): 
    ## Generating the network
    nodes=set_array(node_nr)
    # Nodes list will contain lists indices of connected nodes to each element
    
    for i in range(node_nr):
        a=list(range(node_nr))
        shuffle(a)
        # We shuffle the index list, the connections of current node will be taken from here
        
        nodes[i]=a[:connections+1]
        # We take one more than needed, in case one of the indices point to the neuron itself
        
        tr_prob_setup_flag=True
        for j in range(connections):
            if nodes[i][j]==i:
                tr_prob_setup_flag=False
                nodes[i].remove(i)
                # Remove self-connection
        if tr_prob_setup_flag:
            del nodes[i][-1]
            # If we removed no self-connections, delete the extra index at the end.
    
    ## Setting up transmission probabilities        
    # We established a recurrent network, we need to establish transmission proabability for each connection
    tr_prob_setup_flag=True
    
    if uniform_tr_prob: # The way it is used in the paper is uniform, all connections have equal proabability transmission
        tr_prob_setup_flag=False
        tr_probabilities=[[sigma/connections for j in range(connections)] for i in range(node_nr)]
    
    
    prob_iteration_count=0
    while tr_prob_setup_flag:
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
            tr_prob_setup_flag=False
        if prob_iteration_count>10000: # Deals with the case that C and sigma are inappropriate, prevents infinite loop
            raise ValueError('More than 10.000 iterations when setting up probabilities, terminating. There are >1 probabilities.')
            break
        prob_iteration_count+=1
    #del j,k,a,divider,tr_prob_setup_flag
    # The network is set up with required properties at this point
        
    ## Incorporating time and inputs
    
    outputs=list(np.zeros(node_nr)) # Holds the state of each node.
    activated=[]
    
    for t in range(time_steps):
        
        inputs=outputs # The outputs of the previous iteration are inputs of current.
        outputs=list(np.zeros(node_nr)) 
        
        if single_input_mode and t==0:
            inputs[np.random.randint(0,node_nr-1)]=1 # Pick a random node and activate it in the first frame
        
        for i in range(node_nr):
            for k in range(connections):
                if np.random.random()<spont_prob:              
                    outputs[nodes[i][k]]=1
                elif inputs[i] and np.random.random()<tr_probabilities[i][k]:
                    outputs[nodes[i][k]]=1  # No else statement so if the same node was activated 
                                            # by another connection, it will not be changed.
            if outputs[i]:
                activated.append([t,i])   
                
        ## Plotting individual frames
        
        # Plot individial frames & save img for each round
        if plot_and_save:
            node_nr_sqrt=int(np.sqrt(node_nr))  # Get size of one side of the square to plot
            img = plt.matshow(np.reshape(outputs,[node_nr_sqrt,node_nr_sqrt]), cmap="Greys")
            # Convert to a square matrix and plot      
            
            plt.savefig(images_savedir+"{0:0>3}".format(str(t))+'.jpg')
            plt.close()
        
        # Use ImageJ to generate .avi file from the images.
        # Also possible with cv2 or matplotlib but requires more work.
 
    ## Gathering avalanches        
    if not activated == []: # There is a chance that no avalanches are generated in single input mode
        avalanche_frame_lengths,avalanche_sizes=get_avalanches(activated)    
        all_avalanche_frame_lengths=all_avalanche_frame_lengths+avalanche_frame_lengths
        all_avalanche_sizes=all_avalanche_sizes+avalanche_sizes
#%%
runtime=str(datetime.now()-execution_timer).split('.')[0] # How long the simulations took      
print("{} simulations ran, duration: {}".format(number_of_simulations,runtime))    

#%% Generating log-log plot, Avalanche frame lengths histogram
if not plot_and_save:
    
    if single_input_mode:
        mode='Single input mode'
    else:
        mode='Spontaneous activation mode'
    
    log_max_frames=np.log(max(all_avalanche_frame_lengths))/np.log(log_plot_base)
    # Define the upper border for x axis bins
    plt.figure(figsize=(8,6),dpi=900)                
    plt.hist(all_avalanche_frame_lengths,bins=np.logspace(0,log_max_frames,base=log_plot_base))
    plt.xscale('log',basex=log_plot_base)
    plt.xlabel('Avalanche frame length')
    plt.yscale('log',basey=log_plot_base)
    plt.ylabel('Number of occurences')
    #plt.axvline(x=node_nr,linestyle='--',color="r",label='Node number') # node_nr should be the end of power law relationship
    plt.suptitle('Avalanche frame lengths histogram in log-log axes',fontsize=12,x=0.5,y=.97)
    plt.title('$\sigma$ = {}, Number of runs= {}, Number of nodes= {}\n Time steps= {}, Connection per node= {}, {}'.format(sigma,number_of_simulations,node_nr,time_steps,connections,mode),fontsize=9)
    plt.savefig('/Users/ycan/Desktop/framelengths.png',format='png',dpi=400)
    plt.show()
    
        #%% log-log plot for Avalanche sizes
    log_max_sizes=np.log(max(all_avalanche_sizes))/np.log(log_plot_base)
    # Define the upper border for x axis bins
    plt.figure(figsize=(8,6),dpi=900)                
    plt.hist(all_avalanche_sizes,bins=np.logspace(0,log_max_sizes,base=log_plot_base),color='g')
    plt.xlabel('Avalanche sizes')
    plt.xscale('log',basex=log_plot_base)
    plt.ylabel('Number of occurences')
    plt.yscale('log',basey=log_plot_base)
    #plt.axvline(x=node_nr,linestyle='--',color="r") # Line should be somewhere other than node_nr but where?
    plt.suptitle('Avalanche sizes histogram in log-log axes',fontsize=12,x=0.5,y=0.97)
    plt.title('$\sigma$ = {}, Number of runs= {}, Number of nodes= {}\n Time steps= {}, Connection per node= {}, {}'.format(sigma,number_of_simulations,node_nr,time_steps,connections,mode),fontsize=9)
    plt.savefig('/Users/ycan/Desktop/avalanchesizes.png',format='png',dpi=400)
    plt.show()
