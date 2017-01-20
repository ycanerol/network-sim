#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 17 15:14:50 2017

@author: ycanerol


Network simulator in python

Based off of Beggs Plenz 2003 and Beggs Haldemann 2005 papers


"""

import numpy as np
import matplotlib as plt
from random import shuffle

#Initialization
#Enter and change parameters here

node_nr=64
#avg_connection_per_node=node_nr/10  #To be changed, this is a coarse determination
connections=4   #Defined as C in the paper
sigma=1.2

#%%
def set_array(node_nr):     #Function to set array of empty arrays
    a=[[]for a in range(node_nr)]
    return a

#%% Generating the network
nodes=set_array(node_nr)
#Nodes list will contain lists indices of connected nodes to each element

for i in range(node_nr):
    a=list(range(node_nr))
    shuffle(a)
    #We shuffle the index list, the connections of current node will be taken from here
    
    nodes[i]=a[:connections+1]
    #We take one more than needed, in case one of the indices point to the neuron itself
    
    flag=True
    for j in range(connections):
        if nodes[i][j]==i:
            flag=False
            #print("removed {}\n".format(i))
            nodes[i].remove(i)
            #Remove self-connection
    if flag:
        del nodes[i][-1]
        #If we removed no self-connections, delete the extra index at the end.
        
#We established a recurrent network, we need to establish transmission proabability for each connection
flag=True
while flag:
    tr_probabilities=set_array(node_nr)
    for i in range(node_nr):
        divider=list(np.sort(np.random.random_sample(connections-1)))
        divider.insert(0,0)
        divider.append(1)
        divider=list(np.multiply(divider,sigma)) #Scale the interval to be the size of sigma
        for k in range(1,len(divider)):
            tr_probabilities[i].append(divider[k]-divider[k-1])
            #The constraint is that for each node sigma_i should be equal to sigma
            #Sums of the probabilities for one node should be sigma
            #For this, we divide the sigma into C parts and use the sizes of the parts as probabilities
    all_less_than1=True
    for i in range(node_nr):
        for k in range(connections):
            if tr_probabilities[i][k]>1:
                all_less_than1=False
    if all_less_than1:
        flag=False
                       
del j,k,a,divider,flag
#The network is set up with required properties at this point

#%% Incorporating time and inputs
time_steps=50 #How many times we transmit
spont_prob=0.001

def transmit(prob):
    for i in range(len(prob)):
        if np.random.random()<prob[i]:
            return 1
        else:
            return 0
            
def activate(prob,inputs):
    pass

outputs=[list(np.zeros(connections)) for i in range(node_nr)]

for t in range(time_steps):
    
    inputs=outputs
    outputs=[list(np.zeros(connections)) for i in range(node_nr)]
    
#    for i in range(node_nr):   #Generating a spontaneous input pattern
#        for k in range(connections):
#            if np.random.random()<spont_prob:
#                inputs[i][k]=1
#            else:
#                inputs[i][k]=0     #

    for i in range(node_nr):
        for k in range(connections):
            if np.random.random()<spont_prob:
                outputs[i][k]=1
            elif inputs[i][k]:
                if np.random.random()<tr_probabilities[i][k]:
                    outputs[i][k]=1
            
            
        
        
        
        
        
        
        
        
        
